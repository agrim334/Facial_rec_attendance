<template>
  <div class="home">
    <MarkAttdFaceForm @attdmark='addface'> </MarkAttdFaceForm>
    <div v-if='auto === 0'>
    <form @submit.prevent='addman'>
      <label> Manual </label>
        <div v-for='stud in studlist' :key = 'stud.id'>
          <ManAttdList :stud='stud'> </ManAttdList>
        </div>
      <input type='submit' value = 'Add Records'>
    </form>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import MarkAttdFaceForm from '@/components/AddAttdFaceRec.vue';
import ManAttdList from '@/components/AddAttdManual.vue';

export default {
  name: 'AddAttdFace',
  props: { studlist: Array },
  components: {
    MarkAttdFaceForm,
    ManAttdList,
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
          this.studlist = res.data.studlist;
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
