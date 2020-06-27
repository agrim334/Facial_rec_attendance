<template>
  <div class="home">
    <MarkAttdFaceForm v-if='auto === 1' @attdmark='addface'> </MarkAttdFaceForm>
    <b-form @submit.prevent='addman' v-if='auto === 0'>
      <b-table :items='studlist'>
        <template v-slot:cell(choices)='row'>
          <b-form-radio-group v-model='row.item.status'>
            <b-form-radio value='1'> Present </b-form-radio>
            <b-form-radio value='0'> Absent </b-form-radio>
          </b-form-radio-group>
        </template>
      </b-table>
      <b-button type="submit"> Mark Attendance </b-button>
    </b-form>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import MarkAttdFaceForm from '@/components/AddAttdFaceRec.vue';

export default {
  name: 'AddAttdFace',
  props: { studlist: Array },
  components: {
    MarkAttdFaceForm,
  },
  data() {
    return {
      uid: '',
      cid: '',
      auto: 1,
    };
  },
  methods: {
    addface(attddat) {
      const path = 'http://localhost:5000/attd/add_attd_json';
      this.uid = attddat.rec.uid;
      this.cid = attddat.rec.cid;
      axios.post(path, attddat.rec)
        .then((res) => {
          this.auto = 0;
          if (res.data.status === 'Success') this.uplimg(attddat);
          else alert(res.data.status);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    uplimg(attddat) {
      const path = 'http://localhost:5000/attd/add_attd_json';
      const formData = new FormData();
      for (let i = 0; i < attddat.img.length; i += 1) {
        const tfile = attddat.img[i];
        formData.append('files['.concat(i).concat(']'), tfile);
      }
      formData.append('uid', this.uid);
      formData.append('cid', this.cid);
      axios.post(path, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
        .then((res) => {
          alert(res.data.status);
          this.studlist = res.data.studlist;
          for (let i = 0; i < this.studlist.length; i += 1) {
            this.studlist[i].choices = '';
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addman() {
      const path = 'http://localhost:5000/attd/add_attd_json';
      axios.post(path, {
        studlist: this.studlist,
        uid: this.uid,
        cid: this.cid,
        mancheck: 1,
      })
        .then((res) => {
          console.log(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
