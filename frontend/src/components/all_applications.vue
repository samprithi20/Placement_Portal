<template>
  <div class="container mt-5">

    <div class="d-flex justify-content-between mb-4">
      <h2>All Applications</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/admin')"
      >
        Back
      </button>
    </div>

    <div
      v-for="app in applications"
      :key="app.id"
      class="card p-4 mb-3 shadow-sm"
    >

      <h5>{{ app.student_name }}</h5>

      <hr>

      <p><strong>Company:</strong> {{ app.company_name }}</p>

      <p><strong>Job:</strong> {{ app.job_title }}</p>

      <p><strong>Salary:</strong> {{ app.salary }}</p>

      <p>
        <strong>Status:</strong>
        <span :class="statusClass(app.status)">
          {{ app.status }}
        </span>
      </p>

    </div>

    <div v-if="applications.length === 0" class="text-center mt-5">
      <h5>No applications found</h5>
    </div>

  </div>
</template>

<script>
export default {
  name: "AllApplications",

  data() {
    return {
      applications: []
    }
  },

  methods: {

    async loadApplications() {

      const token = localStorage.getItem("token")

      const res = await fetch(
        "http://127.0.0.1:5000/admin/applications",
        {
          headers: {
            "Authorization": "Bearer " + token
          }
        }
      )

      this.applications = await res.json()
    },

    statusClass(status) {

      if (status === "Placed") return "text-success fw-bold"
      if (status === "Interview Scheduled") return "text-primary fw-bold"
      if (status === "Rejected") return "text-danger fw-bold"
      if (status === "Applied") return "text-secondary fw-bold"

      return ""
    }

  },

  mounted() {
    this.loadApplications()
  }
}
</script>

<style scoped>
.card {
  border-radius: 12px;
}
</style>