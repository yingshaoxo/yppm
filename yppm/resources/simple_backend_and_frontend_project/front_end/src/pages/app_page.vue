<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { global_dict, global_functions } from '../store';

import { ShoppingCartOutlined } from '@ant-design/icons-vue';

import * as app_store_objects_types from '../generated_yrpc/app_store_objects'

const dict = reactive({
  an_app_name: null,
  an_app: new global_dict.app_store_objects.An_App(),
  temp_dict: {
    collapse_key: '0'
  },
})

const functions = reactive({
  refresh_the_app_data: async () => {
    let get_app_detail_request = new global_dict.app_store_objects.Get_App_Detail_Request()
    get_app_detail_request.name = dict.an_app_name

    let response = await global_dict.client.get_app_detail(get_app_detail_request)
    if (response?.an_app != null) {
      dict.an_app = response?.an_app
    }
  },
})

onMounted(async () => {
  dict.an_app_name = global_dict.current_page_data?.name ?? "" 

  await functions.refresh_the_app_data()
})
</script>

<template>
  <a-collapse v-model:activeKey="dict.temp_dict.collapse_key">
    <a-collapse-panel key="1" header="Menu">
      <div class="menu_items">
        <a-button type="primary"
          ghost
          @click="async ()=>{
            await global_functions.go_to_page(global_dict.page_name_dict.home_page)
          }"
        >
          Go_Back
        </a-button>
      </div>
    </a-collapse-panel>
  </a-collapse>

  <!--h1 class="title1">App Store</h1>
  <h3 class="title2"
  >{{ dict.an_app.name }}</h3-->
  <h1 class="title_top">App Store</h1>

  <div class="box">
    <div class="inner_box">
      <p><span class="less_obvious_text">Name</span>: <span class="margin_left">{{ dict.an_app.name }}</span></p>

      <p><span class="less_obvious_text">URL</span>: <a class="margin_left" target="_blank" :href="dict.an_app.url">{{ dict.an_app.url }}</a></p>

      <p><span class="less_obvious_text">Contact</span>: <span class="margin_left">{{ dict.an_app.author_contact_method }}</span></p>

      <p><span class="less_obvious_text margin_bottom">Description</span>: 
        <pre class="margin_top">{{ dict.an_app.description }}</pre>
      </p>

      <!--p>
        <span>Picture</span>:
        <div>
          <a-image v-if="dict.an_app?.id && global_dict.image_dict.has(dict.an_app?.id)" :src="global_dict.image_dict.get(dict.an_app?.id)??undefined" alt="A picture"> </a-image>
        </div>
      </p-->
    </div>
  </div>
</template>

<style lang="less" scoped>
p {
    font-size: 110%;
}

.menu_items {
  ._rows;

  width: 100%;

  justify-content: center;

  > * {
    width: 200px;
    margin-bottom: 10px;

    &:last-child {
      margin-bottom: 0px;
    }
  }
}

.title1 {
  margin-top: 40px;

  opacity: 0.6;

  margin-bottom: 10px;
}

.title2 {
  opacity: 0.5;

  margin-bottom: 40px;
}

.title_top {
  margin-top: 40px;

  opacity: 0.6;

  margin-bottom: 70px;
}

.box {
  ._rows;
  justify-content: start;
  text-align: start;
  .inner_box {
    width: 80%;
  }

  img {
    max-width: 100%;
  }
}

.right_floating_button {
	position:fixed;

  ._center;

	width:40px;
	height:40px;

	bottom:40px;
	right:20px;

	background-color:rgba(239, 83, 80);

	color:#FFF;
  font-weight: bold;

	border-radius:50px;
	text-align:center;
	box-shadow: 2px 2px 3px #999;
}

.left_floating_button {
  .right_floating_button;

  right: auto;
  left: 20px;

	background-color: rgba(245, 127, 23);

  font-size: 150%;
}

.product_list_container {
  ._rows;
  ._responsive;

  width: 100%;
  overflow: auto;
  text-align: start;

  > * {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0px;
    }
  }
  .an_app_box {
    width: 100%;

    img {
      width: 100%;
    }
  }
}

.important_text {
    color: #F57F17
}
.green {
    color: #8BC34A
}
.purple {
    color: #3F51B5
}
.red {
    color: #E91E63
}
.cyan_blue {
    color: #00BFA5
}
.orange {
    color: #F57F17
}
.silver {
    color: #808080
}
.pink {
    color: #F48FB1
}
.less_obvious_text {
    opacity: 60%
}
.smaller_text {
    font-size: 70%;
}

.margin_left {
    margin-left: 8px;
}
.margin_top {
    margin-top: 8px;
}
</style>
