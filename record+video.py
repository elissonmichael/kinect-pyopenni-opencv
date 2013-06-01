#!/usr/bin/python
from openni import *

ctx = Context()
ctx.init()

depth = DepthGenerator()
depth.create(ctx)
video = ImageGenerator()
video.create(ctx)

ctx.start_generating_all()

recorder = Recorder()
recorder.create(ctx)

recorder.destination = "MeuVideo.oni"

recorder.add_node_to_rec(depth, CODEC_16Z_EMB_TABLES)
recorder.add_node_to_rec(video, CODEC_JPEG)

print "Gravando..."
try:
	while True:
	    nRetVal = ctx.wait_one_update_all(depth)

except KeyboardInterrupt:
	recorder.rem_node_from_rec(depth)

ctx.shutdown()
print "Finalizado!"

