# Simple docker app

This is a simple NodeJS based app that only exports a single api endpoint:
`/api/test` which returns a simple JSON output that represents that the app is running.

## Building the image

Simply run the following command:

```bash
# Build the image and call it 'dockerapp'
docker build -t dockerapp .
```

## Testing the image

Simply run the following command:


```bash
# Will run the app at port 3000 locally
docker run -it -p3000:3000 dockerapp
```