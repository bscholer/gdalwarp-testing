# `gdalwarp` Testing

As part of a @dronedeploy project, I needed to test to see how different versions `gdalwarp` handle tectonic transformations.

# Running it
With `docker` installed, just run `make` and it'll take care of the rest!

# Conclusions
_With `gdal 3.10.0, proj 9.5.0`_

TL;DR: The only way to do tectonic transformations with `gdalwarp` appears to be by adding `step proj=set v_4=<src_epoch_here>` to a manually provided proj string, which can be passed in via `-ct`. 

Typically, when transforming coordinates via `pyproj`, you'd create a `Transformer`, and then use it to transform your coordinates. When creating the `Transformer`, you can specify the target epoch, however, you can't specify the source epoch. Then, when calling `.transform()` on the `Transformer`, you specify the `x`, `y`, `z`, and `t`, where `t` is the source epoch.

This means that the proj pipeline definition only includes the target epoch. The problem is that `gdalwarp`'s `-ct` parameter overrides (as demonstrated by this test) `-s_srs`, `-t_srs`, `-s_coord_epoch`, and `-t_coord_epoch`. This means that to specify a source epoch, which is necessary, you must add `step proj=set v_4=<src_epoch_here>` to the beginning of the proj pipeline definition, which manually overrides the `t` parameter for transformations.