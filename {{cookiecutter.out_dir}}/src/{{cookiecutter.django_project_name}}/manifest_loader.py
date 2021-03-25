from manifest_loader.loaders import DefaultLoader


class CustomLoader(DefaultLoader):
    @staticmethod
    def get_multi_match(manifest, pattern):
        if pattern == 'style':
            return list(filter(lambda f: f[-4:] == '.css', manifest.get(pattern)))
        return manifest.get(pattern)
