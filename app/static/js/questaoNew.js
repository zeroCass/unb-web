function questaoNew() {
	const multiplaEscolhaBtn = document.getElementById("multipla_escolha")
	const dissertativaBtn = document.getElementById("dissertativa")
	const campoResposta = document.getElementById("campo_resposta")
	const camposAdicionais = document.getElementById("campos_adicionais")

	function exibirCampoResposta() {
		if (dissertativaBtn.checked) {
			campoResposta.style.display = "none"
			campoResposta.querySelector("input").removeAttribute("required")
		} else {
			campoResposta.style.display = "block"
			campoResposta.querySelector("input").setAttribute("required", "true")
		}
	}

	dissertativaBtn.addEventListener("click", exibirCampoResposta)
	dissertativaBtn.addEventListener("change", exibirCampoResposta)

	function exibirCamposAdicionais() {
		if (multiplaEscolhaBtn.checked) {
			camposAdicionais.style.display = "block"
			camposAdicionais.querySelector("input").setAttribute("required", "true")
		} else {
			camposAdicionais.style.display = "none"
			camposAdicionais.querySelectorAll("input").forEach(function (input) {
				input.removeAttribute("required")
			})
		}
	}

	multiplaEscolhaBtn.addEventListener("click", exibirCamposAdicionais)
	multiplaEscolhaBtn.addEventListener("change", exibirCamposAdicionais)

	const outrosRadioBtns = document.querySelectorAll('input[name="tipo_questao"]')
	outrosRadioBtns.forEach(function (radio) {
		radio.addEventListener("click", function () {
			if (radio.id === "dissertativa") {
				campoResposta.style.display = "none" // Oculta o campo de resposta para o botão "dissertativa"
				camposAdicionais.style.display = "none"
			} else {
				exibirCampoResposta() // Exibe ou oculta o campo de resposta para os outros botões
				exibirCamposAdicionais() // Exibe ou oculta os campos adicionais para o botão "multipla_escolha"
			}
		})
	})
}
