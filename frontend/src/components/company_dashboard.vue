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

    <!-- COMPANY DETAILS -->

    <div class="card p-4 mb-4">

      <div class="d-flex justify-content-between align-items-center mb-3">

        <h4>
          Company Details
        </h4>

        <button
          class="btn btn-warning"
          @click="toggleEdit"
        >
          {{
            editMode
              ? "Cancel"
              : "Edit Profile"
          }}
        </button>

      </div>

      <!-- VIEW MODE -->

      <div v-if="!editMode">

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

        <h5>
          HR Email:
          {{ company.hr_email }}
        </h5>

        <h5>
          Website:
          {{ company.website }}
        </h5>

      </div>

      <!-- EDIT MODE -->

      <div v-else>

        <div class="mb-3">

          <label class="form-label">
            Company Name
          </label>

          <input
            type="text"
            class="form-control"
            v-model="editCompany.company_name"
          >

        </div>

        <div class="mb-3">

          <label class="form-label">
            Industry
          </label>

          <input
            type="text"
            class="form-control"
            v-model="editCompany.industry"
          >

        </div>

        <div class="mb-3">

          <label class="form-label">
            Location
          </label>

          <input
            type="text"
            class="form-control"
            v-model="editCompany.location"
          >

        </div>

        <div class="mb-3">

          <label class="form-label">
            HR Name
          </label>

          <input
            type="text"
            class="form-control"
            v-model="editCompany.hr_name"
          >

        </div>

        <div class="mb-3">

          <label class="form-label">
            HR Email
          </label>

          <input
            type="email"
            class="form-control"
            v-model="editCompany.hr_email"
          >

        </div>

        <div class="mb-3">

          <label class="form-label">
            Website
          </label>

          <input
            type="text"
            class="form-control"
            v-model="editCompany.website"
          >

        </div>

        <button
          class="btn btn-success"
          @click="updateProfile"
        >
          Save Changes
        </button>

      </div>

    </div>

    <!-- STATS -->

    <div class="row mb-4">

      <div class="col-md-4">

        <div class="card p-4 text-center stats-card">

          <h3>{{ stats.total_jobs }}</h3>

          <p>Total Jobs</p>

        </div>

      </div>

      <div class="col-md-4">

        <div class="card p-4 text-center stats-card">

          <h3>{{ stats.total_applications }}</h3>

          <p>Total Applications</p>

        </div>

      </div>

      <div class="col-md-4">

        <div class="card p-4 text-center stats-card">

          <h3>{{ stats.total_placed }}</h3>

          <p>Students Placed</p>

        </div>

      </div>

    </div>

    <!-- ACTION BUTTONS -->

    <div class="d-flex gap-3 flex-wrap">

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

      company: {},

      stats: {

        total_jobs: 0,

        total_applications: 0,

        total_placed: 0

      },

      editMode: false,

      editCompany: {}

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

      this.editCompany = {
        ...data
      }

    },

    async loadStats() {

      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/company/stats",
        {

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      this.stats = data

    },

    toggleEdit() {

      this.editMode = !this.editMode

      this.editCompany = {
        ...this.company
      }

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

          body: JSON.stringify(this.editCompany)

        }
      )

      const data = await response.json()

      alert(data.message)

      this.editMode = false

      this.loadCompany()

    },

    logout() {

      localStorage.removeItem("token")

      localStorage.removeItem("role")

      this.$router.push("/")

    }

  },

  mounted() {

    this.loadCompany()

    this.loadStats()

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