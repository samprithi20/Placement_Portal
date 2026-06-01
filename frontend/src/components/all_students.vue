<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between mb-4">

      <h2>All Students</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/admin')"
      >
        Back
      </button>

    </div>

    <div
      v-for="student in students"
      :key="student.id"
      class="card p-3 mb-3"
    >

      <h5>{{ student.full_name }}</h5>

      <p>
        <strong>Department:</strong>
        {{ student.department }}
      </p>

      <p>
        <strong>CGPA:</strong>
        {{ student.cgpa }}
      </p>

      <p>
        <strong>Graduation Year:</strong>
        {{ student.graduation_year }}
      </p>

    </div>

  </div>

</template>

<script>

export default {

  name: "AllStudents",

  data() {

    return {

      students: []

    }

  },

  methods: {

    async loadStudents() {

      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/admin/students",
        {

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      this.students = data

    }

  },

  mounted() {

    this.loadStudents()

  }

}

</script>