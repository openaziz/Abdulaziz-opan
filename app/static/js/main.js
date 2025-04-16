// Matrix Rain Effect
document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("matrix-canvas")
  if (canvas) {
    const ctx = canvas.getContext("2d")

    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    const katakana =
      "アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン"
    const latin = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    const nums = "0123456789"
    const arabic = "أبتثجحخدذرزسشصضطظعغفقكلمنهوي"

    const alphabet = katakana + latin + nums + arabic

    const fontSize = 16
    const columns = canvas.width / fontSize

    const rainDrops = []

    for (let x = 0; x < columns; x++) {
      rainDrops[x] = 1
    }

    const draw = () => {
      ctx.fillStyle = "rgba(0, 0, 0, 0.05)"
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      ctx.fillStyle = "#0f0"
      ctx.font = fontSize + "px monospace"

      for (let i = 0; i < rainDrops.length; i++) {
        const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length))
        ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize)

        if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          rainDrops[i] = 0
        }
        rainDrops[i]++
      }
    }

    setInterval(draw, 30)
  }

  // زر العودة للأعلى
  const scrollTopButton = document.getElementById("scrollTop")
  if (scrollTopButton) {
    window.addEventListener("scroll", () => {
      if (window.pageYOffset > 300) {
        scrollTopButton.classList.remove("hidden")
      } else {
        scrollTopButton.classList.add("hidden")
      }
    })

    scrollTopButton.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      })
    })
  }

  // نسخ الكود
  const copyButtons = document.querySelectorAll(".copy-code")
  copyButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const codeBlock = this.closest(".code-container").querySelector("pre")
      const textArea = document.createElement("textarea")
      textArea.value = codeBlock.textContent
      document.body.appendChild(textArea)
      textArea.select()
      document.execCommand("copy")
      document.body.removeChild(textArea)

      // إظهار رسالة النسخ
      const originalText = this.innerHTML
      this.innerHTML = '<i class="fas fa-check"></i> تم النسخ'
      setTimeout(() => {
        this.innerHTML = originalText
      }, 2000)
    })
  })

  // تفعيل المودال
  const modalTriggers = document.querySelectorAll("[data-modal]")
  modalTriggers.forEach((trigger) => {
    trigger.addEventListener("click", function () {
      const modalId = this.getAttribute("data-modal")
      const modal = document.getElementById(modalId)
      if (modal) {
        modal.classList.add("active")
      }
    })
  })

  // إغلاق المودال
  const closeButtons = document.querySelectorAll(".close-modal")
  closeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const modal = this.closest(".modal")
      modal.classList.remove("active")
    })
  })

  // إغلاق المودال عند النقر خارجه
  const modals = document.querySelectorAll(".modal")
  modals.forEach((modal) => {
    modal.addEventListener("click", function (e) {
      if (e.target === this) {
        this.classList.remove("active")
      }
    })
  })
})
