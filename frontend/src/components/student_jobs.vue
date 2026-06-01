<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between mb-4">

      <h2>Available Jobs</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/student')"
      >
        Back to Dashboard
      </button>

    </div>

    <div
      v-for="job in jobs"
      :key="job.id"
      class="card p-3 mb-3"
    >

      <h4>{{ job.title }}</h4>

      <p>
        <strong>Company:</strong>
        {{ job.company_name }}
      </p>

      <p>
        <strong>Description:</strong>
        {{ job.description }}
      </p>

      <p>
        <strong>Salary:</strong>
        {{ job.salary }}
      </p>
    <button
      class="btn btn-primary w-100"
      @click="applyJob(job.id)"
      :disabled="job.applied"
    >
      {{ job.applied ? job.application_status : "Apply" }}
    </button>

    </div>

  </div>

</template>

<script>

export default {

  name: "StudentJobs",

  data() {

    return {

      jobs: []

    }

  },

  methods: {

    async loadJobs() {

      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/student/jobs",
        {

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      this.jobs = data

    },

    async applyJob(jobId) {

      const token = localStorage.getItem("token")

      const response = await fetch(
        `http://127.0.0.1:5000/student/apply/${jobId}`,
        {

          method: "POST",

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      alert(data.message)

    }

  },

  mounted() {

    this.loadJobs()

  }

}

</script>

<style scoped>

</style>