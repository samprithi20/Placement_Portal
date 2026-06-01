<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between mb-4">

      <h2>All Jobs</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/admin')"
      >
        Back
      </button>

    </div>

    <div
      v-for="job in jobs"
      :key="job.id"
      class="card p-3 mb-3"
    >

      <h5>{{ job.title }}</h5>

      <p>
        <strong>Company:</strong>
        {{ job.company_name }}
      </p>

      <p>
        <strong>Salary:</strong>
        {{ job.salary }}
      </p>

    </div>

  </div>

</template>

<script>

export default {

  name: "AllJobs",

  data() {

    return {

      jobs: []

    }

  },

  methods: {

    async loadJobs() {

      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/admin/jobs",
        {

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      this.jobs = data

    }

  },

  mounted() {

    this.loadJobs()

  }

}

</script>