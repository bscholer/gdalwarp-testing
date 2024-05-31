# `gdalwarp` Testing

As part of a @dronedeploy project, I needed to test to see how different versions `gdalwarp` handle tectonic transformations.

# Running it
With `docker` installed, just run `make` and it'll take care of the rest!

# Conclusions
The TL;DR is that the only way to actually do tectonic transformations appears to be by adding `step proj=set v_4=<src_epoch_here>`.