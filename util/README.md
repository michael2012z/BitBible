# Utilities

## Dockerfile

If you don't want to borther setting up Sword on your host, use the Dockerfile provided in this folder to build a container.

```bash
cd /PATH/TO/BitBible/util
docker build . -t bitbile
cd /PATH/TO/BitBible
docker run -it -v $(pwd):/root/BitBible bitbible
```

## scripts
- convert_all_sword_modules_to_osis.sh
- - Unzip modules in BitBible/source/sword_modules and convert them into OSIS format. Output XML files are saved in tmp folder.
- convert_all_osis_to_markdown.sh
- - Convert the OSIS XML files in tmp folder into Markdown files (.md) in BitBible/markdown folder.
