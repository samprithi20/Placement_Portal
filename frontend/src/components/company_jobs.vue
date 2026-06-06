<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between mb-4">

      <h2>Posted Jobs</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/company')"
      >
        Back
      </button>

    </div>

    <div
      v-for="job in jobs"
      :key="job.id"
      class="card p-3 mt-3"
    >

      <h5>{{ job.title }}</h5>

      <p>
        Location:
        {{ job.location }}
      </p>

      <p>
        Salary:
        {{ job.salary }}
      </p>

      <p>
        Status:
        {{ job.status }}
      </p>

      <p>
        Applications:
        {{ job.applications }}
      </p>

      <p>
        Deadline:
        {{ job.application_deadline }}
      </p>

      <div class="d-flex gap-2">

        <button
          class="btn btn-primary"
          @click="viewApplications(job.id)"
        >
          View Applications
        </button>

        <button
          class="btn btn-danger"
          @click="closeJob(job.id)"
        >
          Close Job
        </button>

      </div>

    </div>

  </div>

</template>

<script>

export default {

  name: "CompanyJobs",

  data() {

    return {

      jobs: []

    }

  },

  methods: {

    async loadJobs() {

      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/company/jobs",
        {

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      this.jobs = data

    },

    viewApplications(jobId) {

      this.$router.push(
        `/job-applications/${jobId}`
      )

    },

    async closeJob(jobId) {

      const token = localStorage.getItem("token")

      const response = await fetch(
        `http://127.0.0.1:5000/company/close-job/${jobId}`,
        {

          method: "PUT",

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      alert(data.message)

      this.loadJobs()

    }

  },

  mounted() {

    this.loadJobs()

  }

}

</script>

<style scoped>

.card {
  border-radius: 12px;
}

</style>