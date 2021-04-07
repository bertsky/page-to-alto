from lxml import etree as ET

class TextStylesManager():

    def __init__(self):
        self._styles = set()
        self.fields = ('font_family', 'font_type', 'font_width', 'font_size', 'font_color', 'font_style')
        self.output_element = 'TextStyle'

    def get_style_id(self, **kwargs):
        if any(k not in self.fields for k in kwargs):
            raise ValueError(f"Unknown fields in {kwargs}")
        key = '---'.join([str(kwargs.get(x, None)).replace(' ', '%20') for x in self.fields])
        if key not in self.styles:
            self._styles.add(key)
        return key

    @property
    def styles(self):
        ret = {}
        for key in self._styles:
            ret[key] = {}
            vals = key.split('---')
            for field_idx, field in enumerate(self.fields):
                ret[key][field] = vals[field_idx].replace('%20', ' ')
        return ret

    def from_textstyle(self, textstyle):
        kwargs = {}
        print(textstyle)
        kwargs['font_family'] = textstyle.fontFamily
        kwargs['font_type'] = 'serif' if textstyle.serif else 'sans-serif'
        kwargs['font_width'] = 'fixed' if textstyle.monospace else 'proportional'
        if textstyle.fontSize:
            kwargs['font_size'] = textstyle.fontSize
        if textstyle.textColourRgb:
            b = textstyle.textColourRgb // 65336
            g = (textstyle.textColourRgb - (b * 65336)) // 256
            r = textstyle.textColourRgb - (b * 65336) - (g * 256)
            kwargs['font_color'] = '%2x%2x%2x' % (r, g, b)
        if textstyle.textColour:
            # https://en.wikipedia.org/wiki/Web_colors
            rgb = 'ffffff' if textstyle.textColour == 'white' else \
                  '000000' if textstyle.textColour == 'black' else \
                  'ff0000' if textstyle.textColour == 'red' else \
                  '800000' if textstyle.textColour == 'brown' else \
                  '00ffff' if textstyle.fontColour == 'cyan' else \
                  '00ff00' if textstyle.fontColour == 'green' else \
                  '999999' if textstyle.fontColour == 'grey' else \
                  '4b0082' if textstyle.fontColour == 'indigo' else \
                  'ff00ff' if textstyle.fontColour == 'magenta' else \
                  'ffa500' if textstyle.fontColour == 'orange' else \
                  'ff00cb' if textstyle.fontColour == 'pink' else \
                  '40e0d0' if textstyle.fontColour == 'turquoise' else \
                  'ee82ee' if textstyle.fontColour == 'violet' else \
                  'ffff00' if textstyle.fontColour == 'yellow' else \
                  None
            if rgb:
                kwargs['font_color'] = rgb
        font_style = []
        if textstyle.italic:
            font_style.append('italics')
        if textstyle.underlined:
            font_style.append('underline')
        for att in ('bold', 'smallCaps', 'strikethrough', 'subscript', 'superscript'):
            if getattr(textstyle, att):
                font_style.append(att.lower())
        if font_style:
            kwargs['font_style'] = ' '.join(font_style)
        # TODO kerning
        # TODO underlineStyle
        # TODO bgColour
        # TODO bgColourRgb
        # TODO reverseVideo
        # TODO xHeight
        # TODO letterSpaced
        return self.get_style_id(**kwargs)

    def to_xml(self, alto_styles):
        for style_id, style in self.styles.items():
            el_style = ET.SubElement(alto_styles, self.output_element)
            el_style.set('ID', style_id)
            for k, v in style.items():
                if v != 'None':
                    el_style.set(k.replace('_', '').upper(), v)

class ParagraphStyleManager(TextStylesManager):

    def __ini__(self):
        super().__init__()
        self.fields = ('align', 'left', 'right', 'line_space', 'first_line')
        self.output_element = 'ParagraphStyle'