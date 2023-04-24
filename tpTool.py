import sys
import os
import json
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('tpTool 1.3')

        layout = QVBoxLayout()

        # 选择目标文件夹
        self.folder_path = QLineEdit()
        browse_button = QPushButton('选择')
        browse_button.clicked.connect(self.browse_folder)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel('旧版路径：'))
        hbox1.addWidget(self.folder_path)
        hbox1.addWidget(browse_button)
        layout.addLayout(hbox1)

        # 命名规则输入
        self.region = QComboBox()
        self.region.addItems(['01_蒙德_1.0', '01_蒙德_1.0', '02_璃月_1.0', '02_璃月_2.6_层岩巨渊', '03_稻妻_2.0', '03_稻妻_2.4_渊下宫', '04_须弥_3.0_雨林', '04_须弥_3.1_沙漠', '04_须弥_3.1_沙漠', '04_须弥_3.6_苍漠'])
        self.rename = QLineEdit()
        self.tail_number = QLineEdit()
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel('地区：'))
        hbox2.addWidget(self.region)
        hbox2.addWidget(QLabel('名称：'))
        hbox2.addWidget(self.rename)
        hbox2.addWidget(QLabel('尾号：'))
        hbox2.addWidget(self.tail_number)
        layout.addLayout(hbox2)

        # 选择新路径
        self.new_folder_path = QLineEdit()
        new_browse_button = QPushButton('选择')
        new_browse_button.clicked.connect(self.browse_new_folder)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(QLabel('新版路径：'))
        hbox3.addWidget(self.new_folder_path)
        hbox3.addWidget(new_browse_button)
        layout.addLayout(hbox3)

        # 按钮
        run_button = QPushButton('执行')
        run_button.clicked.connect(self.rename_files)
        reset_button = QPushButton('刷新')
        reset_button.clicked.connect(self.clear_inputs)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(run_button)
        hbox4.addWidget(reset_button)
        layout.addLayout(hbox4)

        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory()
        self.folder_path.setText(folder)

    def browse_new_folder(self):
        folder = QFileDialog.getExistingDirectory()
        self.new_folder_path.setText(folder)

    def rename_files(self):
        target_folder = self.folder_path.text()
        new_folder = self.new_folder_path.text()
        region = self.region.currentText()
        rename = self.rename.text()
        tail_number = self.tail_number.text()

        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

        pattern = re.compile(r'^[\u4e00-\u9fa5_a-zA-Z0-9]+$')

        if pattern.match(rename) and tail_number.isdigit():
            files = [f for f in os.listdir(target_folder) if f.endswith('.json')]

            tail_number_int = int(tail_number)
            for i, file in enumerate(files):
                with open(os.path.join(target_folder, file), 'r', encoding='utf-8') as f:
                    data = json.load(f)

                new_tail_number = str(tail_number_int + 1000)[1:]
                new_file_name = f'{region}_{rename}_{new_tail_number}.json'
                new_file_path = os.path.join(new_folder, new_file_name)

                if 'name' in data:
                    data['name'] = new_file_name[:-5]

                with open(new_file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)

                tail_number_int += 1
        else:
            raise ValueError('输入无效，请检查并重新输入')

    def clear_inputs(self):
        self.folder_path.clear()
        self.new_folder_path.clear()
        self.rename.clear()
        self.tail_number.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
