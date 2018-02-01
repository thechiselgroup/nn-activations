const homedir = require('homedir')

exports.fileLocations = {
    imagePath : homedir() + '/.cache/Lodestone/neuralNet/uploads/',
    destinationPath : homedir() + '/.cache/Lodestone/neuralNet/activations/',
    classificationPath : homedir() + '/.cache/Lodestone/neuralNet/classification/',
    pythonPath : './save_activations.py'
}