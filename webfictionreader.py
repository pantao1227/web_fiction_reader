#conding=utf-8
import sys
import zlib
import base64
from os import path
from urllib import request, parse, error
from scrapy import Selector
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit, QFrame, QDockWidget, QMenu
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QPixmap

class OnePageWebEngineView(QWebEngineView):
    def createWindow(self,QWebEnginePage_WebWindowType):
        page = QWebEngineView(self)
        page.urlChanged.connect(self.on_url_changed)
        return page
    def on_url_changed(self,url):
        self.setUrl(url)

class WebFictionReader(QWidget):
    str_prev = ''
    str_next = ''
    str_crnt = ''

    def __init__(self):
        QWidget.__init__(self)
        self.layout_main = QVBoxLayout()
        self.layout_panel = QHBoxLayout()
        self.layout_nav = QHBoxLayout()
        self.line_1 = QFrame(self)
        self.line_1.setFrameShape(QFrame.HLine)
        self.line_1.setFrameShadow(QFrame.Sunken)

        self.wev = OnePageWebEngineView(self)
        self.wev.setZoomFactor(0.8)
        self.dw = QDockWidget(self)
        widget_for_dw = QWidget()
        layout_dw_main = QVBoxLayout()
        layout_dw_btns = QHBoxLayout()
        layout_dw_main.setContentsMargins(0, 0, 0, 0)
        layout_dw_btns.setContentsMargins(0, 0, 0, 0)
        widget_for_dw.setLayout(layout_dw_main)
        layout_dw_main.addWidget(self.wev)
        self.le_dw_search = QLineEdit('', self)
        self.le_dw_search.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid;
            }
            """
        )
        self.btn_dw_load = QPushButton('Load', self)
        self.btn_dw_baidu = QPushButton('Baidu', self)
        layout_dw_btns.addSpacing(10)
        layout_dw_btns.addWidget(self.le_dw_search)
        layout_dw_btns.addSpacing(10)
        layout_dw_btns.addWidget(self.btn_dw_baidu)
        layout_dw_btns.addSpacing(10)
        layout_dw_btns.addWidget(self.btn_dw_load)
        layout_dw_main.addLayout(layout_dw_btns)
        self.dw.setWidget(widget_for_dw)

        self.line_2 = QFrame(self)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.le_url = QLineEdit('https://www.booktxt.net/2_2600/939553.html', self)
        self.te_main = QTextEdit('init',self)
        self.te_main.setReadOnly(True)
        self.lb_title = QLabel('init')
        self.lb_state = QLabel('init')
        self.btn_prev = QPushButton('前', self)
        self.btn_refresh = QPushButton('此', self)
        self.btn_next = QPushButton('次', self)
        # self.layout_main.addWidget(self.le_url)
        self.layout_main.addLayout(self.layout_nav)
        self.layout_main.addWidget(self.dw)
        self.layout_main.addWidget(self.line_1)
        self.layout_nav.addWidget(self.le_url)
        self.layout_nav.addSpacing(10)
        self.layout_nav.addWidget(self.lb_state)
        self.layout_main.addWidget(self.te_main)
        self.layout_main.addWidget(self.line_2)
        self.layout_main.addLayout(self.layout_panel)
        self.layout_panel.addWidget(self.lb_title)
        self.layout_panel.addStretch(1)
        self.layout_panel.addWidget(self.btn_prev)
        self.layout_panel.addSpacing(10)
        self.layout_panel.addWidget(self.btn_refresh)
        self.layout_panel.addSpacing(10)
        self.layout_panel.addWidget(self.btn_next)
        self.setLayout(self.layout_main)
        self.setGeometry(0, 0, 640, 960)
        self.setWindowTitle(u'Reader')
        self.setWindowIcon(icon)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)
        self.layout_panel.setContentsMargins(5, 0, 0, 2)
        self.layout_panel.setSpacing(0)
        self.str_qss_default = """
        QLineEdit {border: none;}
        QWidget {background: #0F2540;color:#d1d1d1;}
        QTextEdit {margin: 0px 5px 0px 5px;border :none;}
        QScrollBar:vertical {border: none;background: #0f2540;width: 5px;}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {color: #0f2540;background: #0f2540;}
        QScrollBar::handle:vertical {border: none;background: #ccc;height: 8px;}
        QScrollBar::sub-page, QScrollBar::add-page {background: #0f2540;}
        """
        str_qss = ''
        with open(path.join(path.dirname(__file__), 'res', 'style.qss'), 'r') as qss_file:
            str_qss = qss_file.read()
        if str_qss == '':
            self.setStyleSheet(self.str_qss_default)
        else:
            self.setStyleSheet(str_qss)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.custom_right_menu)
        self.dw.hide()

        self.btn_prev.clicked.connect(self.btn_prev_clicked)
        self.btn_next.clicked.connect(self.btn_next_clicked)
        self.btn_refresh.clicked.connect(self.btn_refresh_clicked)
        self.le_url.returnPressed.connect(self.le_url_returnPressed)
        self.btn_dw_load.clicked.connect(self.btn_dw_load_clicked)
        self.wev.urlChanged.connect(self.wev_url_changed)
        self.btn_dw_baidu.clicked.connect(self.btn_dw_baidu_clicked)
        self.le_dw_search.returnPressed.connect(self.le_dw_search_returnPressed)

        self.btn_refresh.setFocus()
        # Command argv
        if sys.argv.__len__() >= 2:
            sch = parse.urlparse(sys.argv[1]).scheme
            if sch != '':
                self.le_url.setText(sys.argv[1])
                self.btn_refresh_clicked()

    def custom_right_menu(self, pos):
        menu = QMenu()
        opt1 = menu.addAction("Load Qss File")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == opt1:
            str_qss = ''
            with open(path.join(path.dirname(__file__), 'res', 'style.qss'), 'r') as qss_file:
                str_qss = qss_file.read()
            if str_qss == '':
                self.setStyleSheet(self.str_qss_default)
            else:
                self.setStyleSheet(str_qss)
        return

    def to_html(self,list_t):
        # 读取style文件
        str_css = ''
        with open(path.join(path.dirname(__file__), 'res', 'style.css'), 'r') as css_file:
            str_css = css_file.read()
        # 默认样式
        if str_css == '':
            str_css = """
            html {
                margin:0px;
                padding:0px;
            }
            p {
                font-size:22px;
                line-height:150%;
            }
            """
        str_x_html = """
        <html>
            <head>
                <title>title</title>
            </head>
            <style>
            {}
            </style>
            <body>
        """.format(str_css)
        list_x_html = [str_x_html]
        for i in list_t:
            list_x_html.append('<p>{}</p>\n'.format(i))
        list_x_html.append('</body></html>')
        return ''.join(list_x_html)

    def load_page(self, str_url):
        self.lb_state.setText('Loading...')
        QApplication.processEvents()
        try:
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
                }
            response =  request.urlopen(request.Request(str_url, headers=headers), timeout=3)
        except error.URLError as err:
            self.lb_state.setText(str(err.reason))
            return
        ss = response.read()
        try:
            html = ss.decode('utf=8')
        except:
            try:
                html = ss.decode('gbk')
            except:
                try:
                    decompressed_data = zlib.decompress(ss ,16+zlib.MAX_WBITS)
                    try:
                        html = decompressed_data.decode('utf-8')
                    except:
                        html = decompressed_data.decode('gbk')
                except:
                    self.lb_state.setText('decode error.')
                    return

        sel = Selector(text=html)
        list_txt_t = sel.css('#content::text').extract()
        if list_txt_t == []:
            list_txt_t = sel.css('#booktext::text').extract()
        if list_txt_t == []:
            list_txt_t = sel.css('#htmlContent::text').extract()
        if list_txt_t == []:
            list_txt_t = sel.css('.content p::text').extract()
        if list_txt_t == []:
            list_txt_t = sel.css('#chapterContent::text').extract()
        list_txt = []
        for li in list_txt_t:
            t = li.strip()
            if t != '':
                list_txt.append(t)
        html_disp = self.to_html(list_txt)
        self.te_main.setHtml(html_disp)
        relative_url_next = sel.xpath('.//a[text()="下一章"]/@href').extract_first()
        relative_url_prev = sel.xpath('.//a[text()="上一章"]/@href').extract_first()
        if relative_url_next == None:
            relative_url_next = sel.xpath('.//a[text()="下一章>>"]/@href').extract_first()
        if relative_url_prev == None:
            relative_url_prev = sel.css('.jump').xpath('./a[1]/@href').extract_first()  #cn35k.com
        if relative_url_next == None:
            relative_url_next = sel.xpath('.//a[text()="下一页"]/@href').extract_first()
        if relative_url_prev == None:
            relative_url_prev = sel.xpath('.//a[text()="上一页"]/@href').extract_first()
        self.str_crnt = str_url
        self.str_next = parse.urljoin(self.str_crnt, relative_url_next)
        self.str_prev = parse.urljoin(self.str_crnt, relative_url_prev)
        self.lb_title.setText(sel.xpath('//h1/text()').extract_first().strip())
        self.lb_state.setText('Loaded.')

    def btn_prev_clicked(self):
        self.le_url.setText(self.str_prev)
        self.load_page(self.str_prev)

    def btn_next_clicked(self):
        self.le_url.setText(self.str_next)
        self.load_page(self.str_next)

    def btn_refresh_clicked(self):
        if self.dw.isVisible():
            self.dw.hide()
        self.load_page(self.le_url.text())

    def le_url_returnPressed(self):
        if self.wev.isVisible():
            self.wev.load(QUrl(self.le_url.text()))
        else:
            self.load_page(self.le_url.text())

    def keyPressEvent(self, event):
        if(event.key() == 44):
            self.btn_prev_clicked()
        if(event.key() == 46):
            self.btn_next_clicked()
        if(event.key() == Qt.Key_Q):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                if self.dw.isVisible():
                    self.dw.hide()
                else:
                    if self.wev.url().url() != self.le_url.text():
                        self.wev.load(QUrl(self.le_url.text()))
                    self.dw.show()

    def btn_dw_load_clicked(self):
        self.wev.load(QUrl(self.le_url.text()))

    def wev_url_changed(self):
        self.le_url.setText(self.wev.url().url())

    def btn_dw_baidu_clicked(self):
        self.wev.load(QUrl('https://www.baidu.com/s?wd='+self.le_dw_search.text()))

    def le_dw_search_returnPressed(self):
        self.btn_dw_baidu_clicked()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 以base64存储的icon
    img = b'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'
    img = base64.b64decode(img)
    icon = QPixmap()
    icon.loadFromData(img)
    window = WebFictionReader()
    window.show()
    sys.exit(app.exec_())
