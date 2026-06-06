<template>

  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">

      <h2 class="m-0">Applications</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/company')"
      >
        Back to Dashboard
      </button>

    </div>

    
    <div
      v-for="application in applications"
      :key="application.id"
      class="card p-3 mt-3"
    >


      <h5>
        Student:
        {{ application.student_name }}
      </h5>

      <p>
        Job:
        {{ application.job_title }}
      </p>

      <p>
        Status:
        {{ application.status }}
      </p>

      <p>
        Resume:

        <a
          v-if="application.resume"
          :href="application.resume"
          target="_blank"
        >
          View Resume
        </a>

        <span v-else>
          No Resume Uploaded
        </span>
      </p>

    </div>

  </div>

</template>

<script>

export default {

  name: "CompanyApplications",

  data() {

    return {

      applications: []

    }

  },

  methods: {

    async loadApplications() {

      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/company/applications",
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