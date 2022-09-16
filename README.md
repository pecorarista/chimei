# chimei
文書がどの都道府県の話題について書かれているか、簡易的に判別するプログラム

```bash
pyenv install 3.10.6
pyenv local 3.10.6
pipenv install --python $(pyenv which python3)
pipenv install --dev

# https://www.soumu.go.jp/denshijiti/code.html
mkdir resources
wget https://www.soumu.go.jp/main_content/000730858.xlsx -O resources/000730858.xlsx
```
