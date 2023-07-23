function validInputNumber(value) {
	const regex = new RegExp(/^[0-9]+([.][0-9]+)?/)
	const match = value.match(regex)
	// console.log(match)
	return match ? parseFloat(match[0]) : 0.0
}
