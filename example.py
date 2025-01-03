from enpridener import Prider

p = Prider(filepath="icon_in.png", crop=None)
p.pride("trans", radius=0.5)
p.pride("nonbinary", radius=0.5)
p.pride("lesbian", radius=0.5)
p.pride("ace", radius=0.5)
p.pride("aro", radius=0.5)
p.save("icon_out.png")
p.resize(512).save("icon_out_resized.png")
