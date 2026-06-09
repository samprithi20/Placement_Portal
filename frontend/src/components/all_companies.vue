<template>

  <div class="container mt-5">

    <div class="d-flex justify-content-between mb-4">

      <h2>All Companies</h2>

      <button
        class="btn btn-secondary"
        @click="$router.push('/admin')"
      >
        Back
      </button>

    </div>

    <div
      v-for="company in companies"
      :key="company.id"
      class="card p-3 mb-3"
    >

      <h5>{{ company.company_name }}</h5>

      <p>
        <strong>Industry:</strong>
        {{ company.industry }}
      </p>

      <p>
        <strong>Status:</strong>
        {{ company.approval_status }}
      </p>

      <p>
        <strong>Status:</strong>

        <span v-if="company.is_active" class="text-success">
          Active
        </span>

        <span v-else class="text-danger">
          Deactivated
        </span>
      </p>

      <div class="d-flex gap-2 mt-2">

        <button class="btn btn-warning" @click="deactivateactivate(company.user_id)">
          Deactivate / Activate
        </button>

        <button class="btn btn-danger" @click="blacklistCompany(company.user_id)">
          Blacklist
        </button>

      </div>

    </div>

    

  </div>

</template>

<script>

export default {

  name: "AllCompanies",

  data() {

    return {

      companies: []

    }

  },

  methods: {

    async loadCompanies() {

      const token = localStorage.getItem("token")

      const response = await fetch(
        "http://127.0.0.1:5000/admin/companies",
        {

          headers: {
            "Authorization": "Bearer " + token
          }

        }
      )

      const data = await response.json()

      this.companies = data

    },

    async deactivateactivate(companyId) {

      const token = localStorage.getItem("token")

      const res = await fetch(
        `http://127.0.0.1:5000/admin/deactivate-user/${companyId}`,
        {
          method: "PUT",
          headers: {
            "Authorization": "Bearer " + token
          }
        }
      )

      const data = await res.json()
      alert(data.message)

      this.loadCompanies()
    },

    async blacklistCompany(companyId) {

      const token = localStorage.getItem("token")

      const res = await fetch(
        `http://127.0.0.1:5000/admin/blacklist-user/${companyId}`,
        {
          method: "PUT",
          headers: {
            "Authorization": "Bearer " + token
          }
        }
      )

      const data = await res.json()
      alert(data.message)

      this.loadCompanies()
    }

  },

  mounted() {

    this.loadCompanies()

  }

}

</script>