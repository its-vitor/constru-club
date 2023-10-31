export default function getCouponsPoints() {
  const url = "construclub.squareweb.app";
  const userId = localStorage.key(0);
  const couponsList = document.querySelector("#coupons-list");
  console.log(couponsList);

  async function couponsPoints() {
    let numPage = 1;

    const config = {
      method: "GET",
      headers: {
        Authorization: localStorage.getItem(userId),
      },
    };

    try {
      const req = await fetch(
        `${url}/coupons/points?page=${numPage}`,
        config
      );
      const res = await req.json();
      console.log(res);

      if (res.apiStatus === 200) {
        res.coupons.forEach((coupon) => {
          const newCoupon = document.createElement("li");
          newCoupon.classList =
            "list-unstyled card-text font-weight-bold text-info";
          newCoupon.innerHTML =
            `<i class="fa-solid fa-ticket"></i><span id="user-coupons"> ${coupon}</span>`;
          couponsList.append(newCoupon);
        });
      }
    } catch (error) {
      console.log(error);
    }
  }

  window.addEventListener("load", couponsPoints);
}
