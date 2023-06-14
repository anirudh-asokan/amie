class AdminSpoofMiddleware:
    def resolve(self, next, root, info, **kwargs):
        request = info.context

        # Spoof user for admin purposes.

        return next(root, info, **kwargs)
