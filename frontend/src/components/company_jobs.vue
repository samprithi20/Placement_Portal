<template>

  <div class="container mt-5">

    <h2>Posted Jobs</h2>

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

    }

  },

  mounted() {

    this.loadJobs()

  }

}

</script>