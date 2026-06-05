<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between align-items-center">

      <h2>Student Dashboard</h2>

      <button
        class="btn btn-danger"
        @click="logout"
      >
        Logout
      </button>

    </div>

    <div class="card p-4 mt-4">

      <h5>
        Name:
        {{ student.full_name }}
      </h5>

      <h5>
        Department:
        {{ student.department }}
      </h5>

      <h5>
        CGPA:
        {{ student.cgpa }}
      </h5>

      <h5>
        Graduation Year:
        {{ student.graduation_year }}
      </h5>

      <h5>
        Skills:
        {{ student.skills }}
      </h5>

      <h5>
        Resume:
      </h5>

      <a
        :href="'http://127.0.0.1:5000/uploads/' + student.resume"
        target="_blank"
        class="btn btn-primary"
      >
        View Resume
      </a>

    </div>

    <div class="mt-4 d-flex gap-3 flex-wrap">

      <button
        class="btn btn-primary"
        @click="$router.push('/student-jobs')"
      >
        View Jobs
      </button>

      <button
        class="btn btn-warning"
        @click="$router.push('/my-applications')"
      >
        My Applications
      </button>

      <button
        class="btn btn-info"
        @click="$router.push('/student-edit-profile')"
      >
        Edit Profile
      </button>

      

    </div>

    <div class="mt-3">

      <button
        class="btn btn-secondary"
        @click="loadStudent"
      >
        Refresh
      </button>

    </div>

  </div>

</template>

<script>

export default {

  name: "StudentDashboard",

  data() {

    return {

      student: {},
      csvFileUrl: ""

    }

  },

  methods: {

    async loadStudent() {

      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/student/dashboard",
        {

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      this.student = data

    },


    logout() {

      localStorage.removeItem("token")

      localStorage.removeItem("role")

      this.$router.push("/")

    }

  },

  mounted() {

    this.loadStudent()

  }

}

</script>

<style scoped>

</style>