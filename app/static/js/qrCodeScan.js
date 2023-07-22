function qrCodeScan() {
	function onSucess(decodedText, decodedResult) {
		document.getElementById("qrcode-content").value = decodedText
		document.getElementById("post-form").submit()

		//clear the canvas and removes the reader element
		html5QrcodeScanner.clear()
		document.getElementById("reader").remove()
	}

	function startScanning(cameraId) {
		const html5QrCode = new Html5Qrcode("reader")
		const config = { fps: 10, qrbox: { width: 250, height: 250 } }
		html5QrCode.start(cameraId, config, onSucess)
	}

	// Request camera permission and start scanning
	Html5Qrcode.getCameras()
		.then(devices => {
			// check for back cameras prefer
			const backCamera = devices.find(device => device.label.includes("back"))
			if (backCamera) {
				const backCameraId = backCamera.id
				startScanning(backCameraId)
			} else {
				startScanning(devices[0].id)
			}
		})
		.catch(error => {
			// Handle camera permission error
			console.error("Camera Permission Error:", error)
			// Show an error message to the user
			const errorMessage = "Camera access denied. Unable to start QR code scanning."
			// Display the error message on the page
			const errorElement = document.getElementById("error")
			errorElement.textContent = errorMessage
		})
}
