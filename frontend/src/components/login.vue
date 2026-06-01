<template>

  <div class="container mt-5">

    <h2>Placement Portal Login</h2>

    <div class="mb-3">

      <label>Email</label>

      <input
        type="email"
        v-model="email"
        class="form-control"
      >

    </div>

    <div class="mb-3">

      <label>Password</label>

      <input
        type="password"
        v-model="password"
        class="form-control"
      >

    </div>

    <button
      class="btn btn-primary"
      @click="login"
    >
      Login
    </button>

  

  <div class="mt-3">
    <h9> Student Registration : </h9>

  <button
    class="btn btn-secondary me-2"
    @click="$router.push('/register-student')"
  >
    Register Student
  </button>
<br> 
<br>
<h9>Company Registration : </h9>
  <button
    class="btn btn-secondary"
    @click="$router.push('/register-company')"
  >
    Register Company
  </button>

</div>
</div>

</template>

<script>

export default {

  name: "Login",

  data() {

    return {

      email: "",

      password: ""

    }

  },

  methods: {

    async login() {

      const response = await fetch(
        "http://127.0.0.1:5000/login",
        {

          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({

            email: this.email,

            password: this.password

          })

        }
      )

      const data = await response.json()

      alert(data.message)

      if(data.token){

        localStorage.setItem(
          "token",
          data.token
        )

        localStorage.setItem(
          "role",
          data.role
        )

        if(data.role === "admin"){
          this.$router.push("/admin")
        }

        if(data.role === "student"){
          this.$router.push("/student")
        }

        if(data.role === "company"){
          this.$router.push("/company")
        }

      }

    }

  }

}

</script>

<style scoped>

</style>