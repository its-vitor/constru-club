import ValidarCpf from "./validate-cpf.js";

export default function register() {
  const url = "construclub.squareweb.app";
  const form = document.querySelectorAll("form")[1];
  const erro = document.querySelector("#register-error");
  const { name, email, cpf, password } = form;
  new ValidarCpf(cpf).iniciar();

  async function handleSubmit(e) {
    e.preventDefault();

    const data = {
      name: name.value,
      email: email.value,
      cpf: cpf.value,
      password: password.value,
    };

    const config = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };

    try {
      let numLogin = 0;
      const req = await fetch(`${url}/register`, config);
      const res = await req.json();

      if (res.user_id) {
        location.reload();
        localStorage.setItem(user_id, token)
        erro.classList = "d-none card-text font-weight-bold text-danger";
      } else {
        erro.innerText = res.apiMessage
        erro.classList = "d-block card-text font-weight-bold text-danger";
      }
    } catch (error) {
      console.error("Ocorreu um erro:" + error);
    }
  }

  form.addEventListener("submit", handleSubmit);
}
