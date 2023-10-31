export default function registerCoupon() {
  const url = "https://construclub.squareweb.app";
  const userId = localStorage.key(0)
  const input = document.querySelector("#coupon");
  const submit = document.querySelector("#button-addon2");
  const statusSpan = document.querySelector("#status-coupon")

  async function handleClick(e) {
    e.preventDefault();

    const data = {
      coupon: input.value,
    };

    const config = {
      method: "POST",
      headers: {
        Authorization: localStorage.getItem(userId),
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    };

    try {
      const req = await fetch(`${url}/coupon/register`, config)
      const res = await req.json()

      if (res.apiStatus === 200) {
        statusSpan.innerText = res.apiMessage;
        statusSpan.classList = "d-block card-text font-weight-bold text-success"

        setTimeout(() => {
          location.reload()
        }, 2000)
      } else {
        statusSpan.innerText = res.apiMessage;
        statusSpan.classList = "d-block card-text font-weight-bold text-danger"
      }

    } catch (error) {
      console.log(error)
    }
  }

  submit.addEventListener("click", handleClick);
}
