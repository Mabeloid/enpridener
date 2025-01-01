from PIL import Image, ImageDraw
from typing import Any, Optional

flags = {
    "trans": [{
        "type": "hstripe",
        "colors": ['61c1ff', 'ff8ed3', 'ffffff', 'ff8ed3', '61c1ff']
    }],
    "nonbinary": [{
        "type": "hstripe",
        "colors": ['ffcc01', 'ffffff', 'ee00ff', '000000']
    }],
    "lesbian": [{
        "type": "hstripe",
        "colors": ['d52d00', 'ff9a56', 'ffffff', 'd362a4', 'a30262']
    }],
}

hexstr_to_int = lambda s: int(s, 16) if len(s) == 8 else (int(
    s, 16) << 8) + 0xff if len(s) == 6 else 0

int_to_rgba = lambda i: (
    (i >> 24) & 255,
    (i >> 16) & 255,
    (i >> 8) & 255,
    i & 255,
)

str_to_rgba = lambda s: int_to_rgba(hexstr_to_int(s))


class Prider:

    def __init__(self,
                 filepath: str,
                 crop: Optional[tuple[int, int]] = None) -> None:
        self.image: Image.Image = Image.open(filepath)
        if crop: self.image = self.image.crop(crop)

        if self.image.size[0] != self.image.size[1]:
            cause = "crop" if crop else "image"
            raise ValueError(f"non-square {cause} provided! {self.image.size}")
        self.originalsize = self.image.size[0]

    @staticmethod
    def hstripe(img: Image.Image, size: int, d: dict[str, list[Any]]) -> None:
        colors = d["colors"]
        draw = ImageDraw.Draw(img)
        for i, c in enumerate(colors):
            coords = (0, (size * i) // len(colors))
            coords += (size, (size * (i + 1)) // len(colors))
            draw.rectangle(coords, fill=str_to_rgba(c))

    def genflag(self, flagtype: str, size: int) -> Image.Image:
        img = Image.new("RGBA", (size, ) * 2, 0)
        for d in flags[flagtype]:
            match d["type"]:
                case "hstripe":
                    self.hstripe(img, size, d)
                case _:
                    raise NotImplementedError("unknown type: %s" % d["type"])
        return img

    @staticmethod
    def genmask(size: int) -> Image.Image:
        size *= 4
        mask = Image.new("L", (size, ) * 2, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        size //= 4
        return mask.resize((size, ) * 2)

    def pride(self, flagtype: str, radius: int | float):
        if isinstance(radius, float):
            radius = int(self.originalsize * radius)

        imgsize = self.image.size[0]
        flagimg = self.genflag(flagtype, imgsize + radius)
        mask = self.genmask(imgsize)

        paste_position = (radius // 2, ) * 2
        flagimg.paste(self.image, paste_position, mask)
        self.image = flagimg
        return self

    def resize(self, size: int):
        self.image = self.image.resize((size, ) * 2)
        self.originalsize = size
        return self

    def save(self, *args):
        self.image.save(*args)
        return self


if __name__ == "__main__":
    p = Prider(filepath="icon_in.png", crop=None)
    p.pride("trans", radius=0.5)
    p.pride("nonbinary", radius=0.5)
    p.pride("lesbian", radius=0.5)
    p.save("icon_out.png")
    p.resize(512).save("icon_out_resized.png")
