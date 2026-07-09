<template>

  <div class="container mt-5">

    <h2>Company Registration</h2>

    <div class="mb-3">
      <label>Company Name</label>
      <input type="text" v-model="company_name" class="form-control">
    </div>

    <div class="mb-3">
      <label>Email</label>
      <input type="email" v-model="email" class="form-control">
    </div>

    <div class="mb-3">
      <label>Password</label>
      <input type="password" v-model="password" class="form-control">
    </div>

    <div class="mb-3">
      <label>Industry</label>
      <input type="text" v-model="industry" class="form-control">
    </div>

    <div class="mb-3">
      <label>Location</label>
      <input type="text" v-model="location" class="form-control">
    </div>

    <div class="mb-3">
      <label>Website</label>
      <input type="text" v-model="website" class="form-control">
    </div>

    <div class="mb-3">
      <label>HR Name</label>
      <input type="text" v-model="hr_name" class="form-control">
    </div>

    <div class="mb-3">
      <label>HR Email</label>
      <input type="email" v-model="hr_email" class="form-control">
    </div>

    <button
      class="btn btn-primary"
      @click="registerCompany"
    >
      Register
    </button>

  </div>

</template>

<script>

export default {

  name: "RegisterCompany",

  data() {
    return {
      company_name: "",
      email: "",
      password: "",
      industry: "",
      location: "",
      website: "",
      hr_name: "",
      hr_email: ""
    }

  },

  methods: {

    async registerCompany() {
      const response = await fetch(
        "http://127.0.0.1:5000/register/company",
        {

          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({

            company_name: this.company_name,
            email: this.email,
            password: this.password,
            industry: this.industry,
            location: this.location,
            website: this.website,
            hr_name: this.hr_name,
            hr_email: this.hr_email

          })

        }
      )

      const data = await response.json()

      alert(data.message)

      this.$router.push("/")

    }

  }

}

</script>

