<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between mb-4">

      <h2>Edit Company Profile</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/company')"
      >
        Back
      </button>

    </div>

    <div class="card p-4">

      <div class="mb-3">

        <label>Company Name</label>

        <input
          type="text"
          v-model="company.company_name"
          class="form-control"
        >

      </div>

      <div class="mb-3">

        <label>Industry</label>

        <input
          type="text"
          v-model="company.industry"
          class="form-control"
        >

      </div>

      <div class="mb-3">

        <label>Location</label>

        <input
          type="text"
          v-model="company.location"
          class="form-control"
        >

      </div>

      <div class="mb-3">

        <label>HR Name</label>

        <input
          type="text"
          v-model="company.hr_name"
          class="form-control"
        >

      </div>

      <div class="mb-3">

        <label>Website</label>

        <input
          type="text"
          v-model="company.website"
          class="form-control"
        >

      </div>

      <div class="mb-3">

        <label>HR Email</label>

        <input
          type="email"
          v-model="company.hr_email"
          class="form-control"
        >

      </div>

      <button
        class="btn btn-primary"
        @click="updateProfile"
      >
        Update Profile
      </button>

    </div>

  </div>

</template>

<script>

export default {

  name: "CompanyEditProfile",

  data() {

    return {

      company: {}

    }

  },

  methods: {

    async loadCompany() {

      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/company/dashboard",
        {

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      this.company = data

    },

    async updateProfile() {

      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/company/update-profile",
        {

          method: "PUT",

          headers: {

            "Content-Type": "application/json",

            "Authorization": "Bearer " + token

          },

          body: JSON.stringify(this.company)

        }
      )

      const data = await response.json()

      alert(data.message)

      this.$router.push("/company")

    }

  },

  mounted() {

    this.loadCompany()

  }

}

</script>