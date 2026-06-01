<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between align-items-center mb-4">

      <h2>Company Dashboard</h2>

      <button
        class="btn btn-danger"
        @click="logout"
      >
        Logout
      </button>

    </div>

    <div class="card p-4 mb-4">

      <h4 class="mb-3">
        Company Details
      </h4>

      <h5>
        Company Name:
        {{ company.company_name }}
      </h5>

      <h5>
        Industry:
        {{ company.industry }}
      </h5>

      <h5>
        Status:
        {{ company.approval_status }}
      </h5>

      <h5>
        Location:
        {{ company.location }}
      </h5>

      <h5>
        HR Name:
        {{ company.hr_name }}
      </h5>

    </div>

    <div class="d-flex gap-3">

      <button
        class="btn btn-primary"
        @click="$router.push('/create-job')"
      >
        Post Job
      </button>

      <button
        class="btn btn-success"
        @click="$router.push('/company-jobs')"
      >
        View Posted Jobs
      </button>

      <button
        class="btn btn-warning"
        @click="$router.push('/company-applications')"
      >
        View Applications
      </button>

    </div>

  </div>

</template>

<script>

export default {

  name: "CompanyDashboard",

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

    logout() {

      localStorage.removeItem("token")

      localStorage.removeItem("role")

      this.$router.push("/")

    }

  },

  mounted() {

    this.loadCompany()

  }

}

</script>

<style scoped>

.card {
  border-radius: 12px;
}

button {
  min-width: 150px;
}

</style>