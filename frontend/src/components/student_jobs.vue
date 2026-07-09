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

      <p>
        <strong>Status:</strong>
        {{ job.status }}
      </p>

      <p
        v-if="job.message"
        class="mt-2 fw-bold"
        :class="job.applied ? 'text-success' : 'text-danger'"
      >
        {{ job.message }}
      </p>

      <button
        class="btn btn-primary"
        @click="applyJob(job.id)"
        :disabled="!job.is_eligible || job.applied || job.status === 'closed'"
      >
        {{
          job.status === "closed"
            ? "Closed"
            : job.applied
              ? "Applied"
              : job.is_eligible
                ? "Apply"
                : "Not Eligible"
        }}
      </button>

      <p v-if="!job.is_eligible" class="text-danger mt-2">
        {{ job.eligibility_message || "Eligibility criteria not matching" }}
      </p>

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
      this.jobs = data.map(job => ({...job,
        message: ""
      }))
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

      const job = this.jobs.find(
        j => j.id === jobId
      )

      job.message = data.message

      if (response.ok) {

        job.applied = true

      }

    }
  },

  mounted() {
    this.loadJobs()
  }
}
</script>