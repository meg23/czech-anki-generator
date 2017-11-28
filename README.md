# Czech sentence grabber for Anki

If you are attempting to practice your Czech listening skills, you know by now how hard it is to find simple Czech sentences with matching audio. Project syndicate is a Prague based organization that distributes simple articles in multiple languages including Czech. Articles mainly pertain to current events and opinions. 

The purpose of this script is pull Czech articles from www.project-syndicate.org, tokenize the sentences, and send sentences to google translate both for audio and translation. Finally, the script takes this data and generates an Anki deck containing the following data:

* Czech Sentence with Slow Czech Audio in MP3 format
* English Translation 

The goal is to improve your listening skills by reviewing these cards. 

## Getting Started

Install requirements:

```
pip install -r requirements.txt
```

Next, you can execute the script:

```
python czech-anki-generator.py
````

After this completes, you should see czech-sentences.apkg along with all the accompanying audio files in your local directory. This file can be imported directly into Anki. Audio files will be automatically bundled into the Anki deck. 

## Resources

* [Project Syndicate](http://www.project-syndicate.org/archive?language=czech) - Simple article archive for Czech
* [Anki](https://ankiweb.net/about) - Flashcard learning tool

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

