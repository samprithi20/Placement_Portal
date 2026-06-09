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

      <p>
        <strong>Status:</strong>

        <span v-if="student.is_active" class="text-success">
          Active
        </span>

        <span v-else class="text-danger">
          Deactivated
        </span>
      </p>

      <p>
        <strong>Resume:</strong>

        <a
          v-if="student.resume"
          :href="'http://127.0.0.1:5000/uploads/' + student.resume"
          target="_blank"
        >
          View Resume
        </a>

        <span v-else>
          No Resume Uploaded
        </span>
      </p>

      <div class="d-flex gap-2 mt-2">

      <button class="btn btn-warning" @click="deactivateactivate(student.user_id)">
        Deactivate / Activate
      </button>

      <button class="btn btn-danger" @click="blacklist(student.user_id)">
        Blacklist
      </button>

    </div>

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

    },
    async deactivateactivate(userId) {

      const token = localStorage.getItem("token")

      const res = await fetch(
        `http://127.0.0.1:5000/admin/deactivate-user/${userId}`,
        {
          method: "PUT",
          headers: {
            "Authorization": "Bearer " + token
          }
        }
      )

      const data = await res.json()
      alert(data.message)

      this.loadStudents()
    },

    async blacklist(userId) {

      const token = localStorage.getItem("token")

      const res = await fetch(
        `http://127.0.0.1:5000/admin/blacklist-user/${userId}`,
        {
          method: "PUT",
          headers: {
            "Authorization": "Bearer " + token
          }
        }
      )

      const data = await res.json()
      alert(data.message)

      this.loadStudents()
    }

  },

  mounted() {

    this.loadStudents()

  }

}

</script>