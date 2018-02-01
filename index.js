const config = require('./config.js')
const child_process = require('child_process')
const fs = require('fs')
const numpy_parser = require('numpy-parser')

exports.testPkg = (message) => {
    console.log('testing, testing, 123', message)
}

exports.classifyImage = (imageFile) => {
	return new Promise((resolve, reject) => {
		const saveActivations = child_process.spawn('python', [config.fileLocations.pythonPath, imageFile, config.fileLocations.destinationPath, config.fileLocations.classificationPath])

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
		fs.readFile(fileLocations.classificationPath + 'top5.json', (err, data) => {
			if (err) {
				console.error('Could not read file! ' + err)
			} else {
				resolve(JSON.parse(data))
			}
		})
	})
}