## Thumbnail server

[pilbox extension](http://agschwender.github.io/pilbox/#extension) to generate thumbnails out static files stored in a configured s3 bucket.  Will run in fargate behind cloudfront.  Runs on `http://localhost:8888/` by default.

Only one URL pattern is supported `http://localhost:8888/{mode}/{width}x{height}/{collection_id}/{md5}`

`mode` is `clip`, `crop`, `fill`, or `scale`

## Docker setup

```
docker build -t thumbnailer .
docker compose up -d
localhost:8888/<mode>/<width>x<height>/<collection_id>/<md5> (ex: http://localhost:8888/clip/500x500/12903/05b191ddf0e0353b04b6a44b91e680b2)
```

```
S3_ENDPOINT=... thumbnail.py --position=face

python thumbnail.py --help
Usage: thumbnail_server [OPTIONS]

Options:

  --allowed_hosts                  valid hosts (default [])
  --allowed_operations             valid ops (default [])
  --background                     default hexadecimal bg color (RGB or ARGB)
  --client_key                     client key
  --client_name                    client name
  --config                         path to configuration file
  --content_type_from_image        override content type using image mime type
  --debug                          run in debug mode (default False)
  --expand                         default to expand when rotating
  --filter                         default filter to use when resizing
  --format                         default format to use when outputting
  --help                           show this help information
  --implicit_base_url              prepend protocol/host to url paths
  --max_requests                   max concurrent requests (default 40)
  --mode                           default mode to use when resizing
  --operation                      default operation to perform
  --optimize                       default to optimize when saving
  --port                           run on the given port (default 8888)
  --position                       default cropping position
  --quality                        default jpeg quality, 0-100
  --timeout                        request timeout in seconds (default 10)
  --validate_cert                  validate certificates (default True)

site-packages/tornado/log.py options:

  --log_file_max_size              max size of log files before rollover
                                   (default 100000000)
  --log_file_num_backups           number of log files to keep (default 10)
  --log_file_prefix=PATH           Path prefix for log files. Note that if you
                                   are running multiple tornado processes,
                                   log_file_prefix must be different for each
                                   of them (e.g. include the port number)
  --log_to_stderr                  Send log output to stderr (colorized if
                                   possible). By default use stderr if
                                   --log_file_prefix is not set and no other
                                   logging is configured.
  --logging=debug|info|warning|error|none 
                                   Set the Python log level. If 'none', tornado
                                   won't touch the logging configuration.
                                   (default info)

```

## Configuration

`S3_ENDPOINT` specifies an https URL to an s3 bucket path, ex: "https://s3-us-west-2.amazonaws.com/static-ucldc-cdlib-org/harvested_images" or "https://s3-us-west-2.amazonaws.com/rikolti-content/thumbnails"