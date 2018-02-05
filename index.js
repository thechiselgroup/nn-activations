const child_process = require('child_process')
const fs = require('fs')
const numpy_parser = require('numpy-parser')
const homedir = require('homedir')
const path = require('path')
const check_python = require('check-python')

const fileLocations = {
    destinationPath : homedir() + '/.cache/Lodestone/neuralNet/activations/',
    classificationPath : homedir() + '/.cache/Lodestone/neuralNet/classification/',
    pythonPath : path.resolve(__dirname, 'save_activations.py')
}

var python = 'python'
check_python((err, pythonPath, ver) => {
	if(err) {
		throw(err)
	} else if(ver.indexOf("3.") === 0) {
		python = "python2"
	} else {
		python = pythonPath
	}

	const command = python + " --version"
	child_process.exec(command, (err, stdout, stderr) => {
		if(err) {
			throw(err)
		}
		//For some reason, the expected output comes through stderr
		console.log('Using python version: ' + stderr)
	})
})

exports.classifyImage = (imageFileName) => {
	return new Promise((resolve, reject) => {
		imageHash = imageFileName.slice(-32)
		fileLocations.destinationPath.concat(imageHash, '/')
		fileLocations.classificationPath.concat(imageHash, '/')

		const saveActivations = child_process.spawn(python, [fileLocations.pythonPath, imageFileName, fileLocations.destinationPath, fileLocations.classificationPath])

		saveActivations.on('exit', (code) => {
			resolve(code)
		})

		saveActivations.stderr.on('data', (data) => {
			console.error(data)
			reject(data)
		})
	})
}

exports.readResults = () => {
	return new Promise((resolve, reject) => {
		fs.readdir(fileLocations.destinationPath, (err, files) => {
			if (err) {
				console.error('Could not read directory! ' + err)
			} else {
				files.sort((a, b) => {
					return new Number (a.split('_')[0]) - new Number (b.split('_')[0])
				})
				resolve(Promise.all(files.map((file) => {
					return new Promise((resolve, reject) => {
						fs.readFile(path.join(fileLocations.destinationPath, file), (err, data) => {
							if (err) {
								console.error('Could not read files! ' + err)
							} else {
								resolve(numpy_parser.fromArrayBuffer(new Uint8Array(data).buffer))
							}
						})
					})
				})))
			}
		})
	})
}

exports.readClassification = () => {
	return new Promise((resolve, reject) => {
		fs.readFile(path.join(fileLocations.classificationPath, 'top5.json'), (err, data) => {
			if (err) {
				console.error('Could not read file! ' + err)
			} else {
				resolve(JSON.parse(data))
			}
		})
	})
}