## Create a lambda layer and upload to AWS

```bash
pip install pyjwt -t python/

zip -r layer.zip python/

aws lambda publish-layer-version --layer-name pyjwt --zip-file fileb://layer.zip --compatible-runtimes python3.13
```