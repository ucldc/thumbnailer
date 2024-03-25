#!/usr/bin/env python
""" thumbnail server for md5s3stash
extension to pilbox server http://agschwender.github.io/pilbox/#extension
"""
import tornado.gen
from pilbox.app import PilboxApplication, ImageHandler, main
import os

assert 'S3_ENDPOINT' in os.environ, "`S3_ENDPOINT` must be set"


class ThumbnailApplication(PilboxApplication):
    def get_handlers(self):
        # URL regex to handler mapping
        return [
            (r"^/([^/]+)/(\d+)x(\d+)/(\d+)/([a-fA-F\d]{32})$", ThumbnailImageHandler),
            (r"^/([^/]+)/(\d+)x(\d+)/(\d+)/.*$", ThumbnailImageHandler)
        ]
        #            mode, w, h, collection_id, md5


class ThumbnailImageHandler(ImageHandler):
    def prepare(self):
        self.args = self.request.arguments.copy()
        self.settings['content_type_from_image'] = True

    @tornado.gen.coroutine
    def get(self, mode, w, h, collection_id, md5):
        url = f"{os.getenv('S3_ENDPOINT')}/{collection_id}/{md5}"
        self.args.update(dict(w=w, h=h, url=url, mode=mode))
        self.validate_request()
        resp = yield self.fetch_image()
        resp.headers["Cache-Control"] = "public, max-age=31536000"
        self.render_image(resp)


    def get_argument(self, name, default=None):
        return self.args.get(name, default)


if __name__ == "__main__":
    main(app=ThumbnailApplication(timeout=30,))
