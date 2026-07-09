<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between align-items-center mb-4">

      <h2>Admin Dashboard</h2>

      <button class="btn btn-danger"
        @click="logout"> Logout </button>

    </div>

    <div class="card p-4 mb-4">
      <h4 class="mb-3">
        Portal Statistics
      </h4>

      <h5>
        Total Students:
        {{ dashboard.total_students }}
      </h5>

      <h5>
        Total Companies:
        {{ dashboard.total_companies }}
      </h5>

      <h5>
        Total Jobs:
        {{ dashboard.total_jobs }}
      </h5>

      <h5>
        Pending Companies:
        {{ dashboard.pending_companies }}
      </h5>

      <h5>
        Pending Jobs: 
        {{  dashboard.pending_jobs }}
      </h5>

    </div>

    <div class="d-flex gap-3 mb-4">
      <button
        class="btn btn-primary"
        @click="$router.push('/all-students')"
      > View Students </button>

      <button class="btn btn-success"
        @click="$router.push('/all-companies')"
      > View Companies </button>

      <button class="btn btn-secondary"
        @click="$router.push('/all-jobs')"
      > View Jobs </button>

      <button class="btn btn-info"
        @click="$router.push('/reports')"
      > View Reports </button>

    </div>

    <h3 class="mb-3"> Pending Companies </h3>

    <div v-for="company in companies"
      :key="company.id"
      class="card p-3 mb-3"
    >
      <h5>
        {{ company.company_name }}
      </h5>

      <p>
        <strong>Industry:</strong>
        {{ company.industry }}
      </p>

      <p>
        <strong>HR Name:</strong>
        {{ company.hr_name }}
      </p>

      <p>
        <strong>HR Email:</strong>
        {{ company.hr_email }}
      </p>

      <button class="btn btn-success"
        @click="approveCompany(company.id)"
      > Approve </button>
      <br>
      <button class="btn btn-danger"
        @click="rejectCompany(company.id)"
      > Reject </button>

    </div>

    <h3 class="mb-3 mt-5"> Pending Jobs </h3>

    <div v-for="job in jobs"
      :key="job.id"
      class="card p-3 mb-3"
    >
      <h5>
        {{ job.title }}
      </h5>

      <p>
        <strong>Company:</strong>
        {{ job.company_name }}
      </p>

      <p>
        <strong>Location:</strong>
        {{ job.location }}
      </p>

      <p>
        <strong>Salary:</strong>
        {{ job.salary }}
      </p>

      <div class="d-flex gap-2">
        <button class="btn btn-success"
          @click="approveJob(job.id)"
        > Approve Job </button>

        <button class="btn btn-danger"
          @click="rejectJob(job.id)"
        > Reject Job </button>
      </div>

    </div>

</div>

</template>
<script>

export default {
  name: "AdminDashboard",
  data() {
    return {
      dashboard: {
        total_students: 0,
        total_companies: 0,
        total_jobs: 0,
        pending_companies: 0,
        pending_jobs: 0

      },
      companies: [],
      jobs: []
    }
  },

  methods: {

    async loadDashboard() {
      const token = localStorage.getItem("token")
      const response = await fetch(
        "http://127.0.0.1:5000/admin/dashboard",
        {
          headers: {
            "Authorization": "Bearer " + token
          }
        }
      )
      const data = await response.json()
      this.dashboard = data
    },

    async loadPendingCompanies() {
      const token = localStorage.getItem("token")
      const response = await fetch(
        "http://127.0.0.1:5000/admin/pending-companies",
        {
          headers: {
            "Authorization": "Bearer " + token
          }
        }
      )
      const data = await response.json()
      this.companies = data
    },

    async approveCompany(companyId) {
      const token = localStorage.getItem("token")
      const response = await fetch(
        `http://127.0.0.1:5000/admin/approve-company/${companyId}`,
        {
          method: "PUT",
          headers: {
            "Authorization": "Bearer " + token
          }
        }
      )

      const data = await response.json()
      alert(data.message)
      this.loadDashboard()
      this.loadPendingCompanies()
    },
    async rejectCompany(companyId) {
      const token = localStorage.getItem("token")
      const response = await fetch(
        `http://127.0.0.1:5000/admin/reject-company/${companyId}`,
        {
          method: "DELETE",
          headers: {
            "Authorization": "Bearer " + token
          }
        }
      )

      const data = await response.json()
      alert(data.message)

      this.loadDashboard()
      this.loadPendingCompanies()
    },

    async loadPendingJobs() {
      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/admin/pending-jobs",
        {
          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()
      this.jobs = data

    },

    async approveJob(jobId) {
      const token = localStorage.getItem("token")
      const response = await fetch(
        `http://127.0.0.1:5000/admin/approve-job/${jobId}`,
        {
          method: "PUT",
          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      alert(data.message)

      this.loadPendingJobs()
      this.loadDashboard()
    },

    async rejectJob(jobId) {
      const token = localStorage.getItem("token")

      const response = await fetch(
        `http://127.0.0.1:5000/admin/reject-job/${jobId}`,
        {
          method: "DELETE",
          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )
      const data = await response.json()

      alert(data.message)

      this.loadPendingJobs()
    },

    logout() {
      localStorage.removeItem("token")
      localStorage.removeItem("role")
      this.$router.push("/")
    }

  },

  mounted() {

    this.loadDashboard()
    this.loadPendingCompanies()
    this.loadPendingJobs()
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