#!/usr/bin/env python3
"""制作看板生成脚本：把 BOARD 数据塞进 template.html，生成看板 HTML。

用法：
  python3 build_board.py board.js 输出.html "项目名 制作看板"   # 生成 / 回改后重新生成
  python3 build_board.py --extract 现有看板.html > board.js      # 从已有看板里取出 BOARD 数据，用来回改

board.js 里写 `const BOARD = { ... };`（也可以只写 `{ ... }`）。
template.html 里内嵌了风格库截图，体积大，不要整份读进上下文，也不要手抄。
"""
import pathlib, sys

A = '/* ==== BOARD DATA START ==== */'
B = '/* ==== BOARD DATA END ==== */'
TPL = pathlib.Path(__file__).resolve().parent.parent / 'template.html'


def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == '--extract':
        src = pathlib.Path(args[1]).read_text(encoding='utf-8')
        i, j = src.index(A) + len(A), src.index(B)
        sys.stdout.write(src[i:j].strip() + '\n')
        return
    if len(args) < 2:
        sys.exit(__doc__)
    tpl = TPL.read_text(encoding='utf-8')
    board = pathlib.Path(args[0]).read_text(encoding='utf-8').strip()
    if not board.startswith('const BOARD'):
        board = 'const BOARD = ' + board.rstrip().rstrip(';') + ';'
    i, j = tpl.index(A) + len(A), tpl.index(B)
    out = tpl[:i] + '\n' + board + '\n' + tpl[j:]
    if len(args) > 2:
        out = out.replace('<title>制作看板</title>', '<title>' + args[2] + '</title>', 1)
    pathlib.Path(args[1]).write_text(out, encoding='utf-8')
    print(f'已生成 {args[1]}（{len(out) // 1024} KB）')


if __name__ == '__main__':
    main()
