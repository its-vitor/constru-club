export default function login() {
  const url = "construclub.squareweb.app";
  const form = document.querySelectorAll("form")[0];
  const erro = document.querySelector("#login-error");
  const { email, password } = form;

  async function handleSubmit(e) {
    e.preventDefault();

    const data = {
      email: email.value,
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
      const req = await fetch(`${url}:80/login`, config);
      const res = await req.json();

      if (res.user_id) {
        window.location = `${url}:5500/score.html`;
        localStorage.setItem(res.user_id, res.token);
        erro.classList = "d-none card-text font-weight-bold text-danger";
      } else {
        erro.innerText = res.apiMessage;
        erro.classList = "d-block card-text font-weight-bold text-danger";
      }
    } catch (error) {
      console.error(error);
    }
  }

  function handleLoad() {
    if (localStorage.length > 0) {
      window.location = `${url}:5500/score.html`;
    }
  }

  form.addEventListener("submit", handleSubmit);
  window.addEventListener("load", handleLoad);
}
