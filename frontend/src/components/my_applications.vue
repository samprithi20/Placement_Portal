<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between align-items-center mb-4">

      <h2>My Applications</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/student')"
      >
        Back
      </button>

    </div>

    <div
      v-for="application in applications"
      :key="application.job_title"
      class="card p-3 mb-3"
    >

      <h4>
        {{ application.job_title }}
      </h4>

      <h5>
        Company:
        {{ application.company_name }}
      </h5>

      <p>
        Status:
        {{application.status
          ? application.status
          : "Applied"}}
      </p>

      <p>
        Interview Date:
        {{
          application.interview_date !== "Not Scheduled"
            ? new Date(application.interview_date).toLocaleString()
            : "Not Scheduled"
        }}
      </p>

      <p>
        Feedback:
        {{ application.feedback || "No Feedback Yet" }}
      </p>

    </div>

  </div>

</template>

<script>

export default {

  name: "MyApplications",

  data() {

    return {

      applications: []

    }

  },

  methods: {

    async loadApplications() {

      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/student/my-applications",
        {

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      this.applications = data

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