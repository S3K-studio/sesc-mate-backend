from telegram_handler.formatters import HtmlFormatter
import html


class FixedHtmlFormatter(HtmlFormatter):
    def format(self, record):
        s = super(FixedHtmlFormatter, self).format(record)
        if record.exc_info:
            s += '\n' + self.formatException(record.exc_info)
        return s

    def formatException(self, *args, **kwargs):
        s = super(HtmlFormatter, self).formatException(*args, **kwargs)
        return f"<pre>{html.escape(s)}</pre>"
