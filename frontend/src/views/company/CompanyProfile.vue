<script setup>
import CompanyNavbar from '../../components/CompanyNavbar.vue'
import {ref,onMounted} from 'vue'
import api from '../../api'

const token=localStorage.getItem('token')
const company=ref({})
const showEditModal = ref(false)

const fetchProfile=async()=>{
 const res=await api.get('/company/profile',{
 headers:{Authorization:`Bearer ${token}`}
 })
 company.value=res.data
}

const updateProfile = async () => {

await api.put(

    "/company/profile",

    company.value,

    {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

)

showEditModal.value = false

await fetchProfile()

}

onMounted(fetchProfile)
</script>

<template>
<CompanyNavbar/>

<div class="container mt-4">

<div class="card shadow-sm p-4">

<h2>{{company.company_name}}</h2>

<p><b>Status:</b> {{company.approval_status}}</p>

<hr>

<h4>Company Details</h4>

<p><b>Industry:</b> {{company.industry}}</p>
<p><b>Location:</b> {{company.location}}</p>
<p><b>Website:</b> {{company.website}}</p>
<p><b>Description:</b> {{company.description}}</p>

<hr>

<h4>HR Details</h4>

<p><b>Name:</b> {{company.hr_name}}</p>
<p><b>Email:</b> {{company.hr_email}}</p>
<p><b>Contact:</b> {{company.hr_contact}}</p>

<button
class="btn btn-primary"
@click="showEditModal = true"
>
Edit Profile
</button>

</div>

</div>
<div
    v-if="showEditModal"
    class="modal d-block"
    style="background: rgba(0,0,0,.5);"
>
    <div class="modal-dialog modal-lg">
        <div class="modal-content">

            <div class="modal-header">
                <h4>Edit Company Profile</h4>

                <button
                    class="btn-close"
                    @click="showEditModal = false"
                ></button>
            </div>

            <div class="modal-body">

                <label>Company Name</label>
                <input
                    class="form-control mb-3"
                    v-model="company.company_name"
                >

                <label>Industry</label>
                <input
                    class="form-control mb-3"
                    v-model="company.industry"
                >

                <label>Location</label>
                <input
                    class="form-control mb-3"
                    v-model="company.location"
                >

                <label>Website</label>
                <input
                    class="form-control mb-3"
                    v-model="company.website"
                >

                <label>Description</label>
                <textarea
                    class="form-control mb-3"
                    v-model="company.description"
                ></textarea>

                <label>HR Name</label>
                <input
                    class="form-control mb-3"
                    v-model="company.hr_name"
                >

                <label>HR Email</label>
                <input
                    class="form-control mb-3"
                    v-model="company.hr_email"
                >

                <label>HR Contact</label>
                <input
                    class="form-control mb-3"
                    v-model="company.hr_contact"
                >

            </div>

            <div class="modal-footer">

                <button
                    class="btn btn-secondary"
                    @click="showEditModal = false"
                >
                    Cancel
                </button>

                <button
                    class="btn btn-primary"
                    @click="updateProfile"
                >
                    Save Changes
                </button>

            </div>

        </div>
    </div>
</div>
</template>
