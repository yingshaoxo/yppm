<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { global_dict, global_functions } from '../store';

import type * as app_store_objects_types from '../generated_yrpc/app_store_objects'

const an_app_reference =  new global_dict.app_store_objects.An_App()

const dict = reactive({
  a_product: new global_dict.app_store_objects.An_App(),
  temp_dict: {
    collapse_key: '0'
  },
  search_input: "",
  pagination: {
    current: 1,
    size: 10,
    total: 1000,
  },
  app_list: [] as app_store_objects_types.An_App[],
  column_name: [
    {
      title: 'Name',
      dataIndex: an_app_reference._key_string_dict.name,
      key: 'name',
      align: 'center',
      ellipsis: true,
      width: 100,
      // fixed: 'left'
    },
    {
      title: 'Description',
      dataIndex: an_app_reference._key_string_dict.description,
      key: 'description',
      align: 'center',
      width: 100,
      ellipsis: true,
      // fixed: 'left'
    },
    /*
    {
      title: 'Clicks',
      dataIndex: an_app_reference._key_string_dict.price,
      key: 'click_number',
      align: 'center',
      width: 100,
      responsive: ["sm"]
    },
    */
  ],
})

const functions = reactive({
  refresh_app_list: async () => {
    let search_app_request = new global_dict.app_store_objects.Search_App_Request()
    search_app_request.search_input = dict.search_input
    search_app_request.page_size = dict.pagination.size
    search_app_request.page_number = dict.pagination.current - 1

    let response = await global_dict.client.search_app(search_app_request)
    if (response?.app_list != null) {
      dict.app_list = response?.app_list
    }
  }, 
  on_row_click: async (record: app_store_objects_types.An_App) => {
    await global_functions.go_to_page(global_dict.page_name_dict.app_page, {
      name: record.name
    })
  }
})

onMounted(async () => {
  await functions.refresh_app_list()
})
</script>

<template>
  <a-collapse v-model:activeKey="dict.temp_dict.collapse_key">
    <a-collapse-panel key="1" header="Menu">
      <div class="menu_items">
        <a-button type="primary"
          ghost
          @click="async ()=>{
            await global_functions.print('This website was made by @yingshaoxo.\n\nIt is a template in YPPM (Yingshaoxo Python Package Manager).')
          }"
        >
          About
        </a-button>
      </div>
    </a-collapse-panel>
  </a-collapse>

  <h1 class="title">App Store</h1>

  <a-input-search
    class="search_box"
    v-model:value="dict.search_input"
    placeholder="Let's do a search"
    size="large"
    style="width: 60%"
    @search="async () => {
      await functions.refresh_app_list()
    }"
  />

  <div class="a_table">
    <a-table class="mb-[24px]" bordered :data-source="dict.app_list" :columns="dict.column_name" :pagination="false"
      :scroll="{ x: '1500' }"
      :customRow="(record: any) => {
        return {
            onClick: (_event: PointerEvent) => {
                functions.on_row_click(record)
            }
        }
      }"
    >
    </a-table>
  </div>
  
  <div class="page_jumper">
    <a-pagination
      v-model:current="dict.pagination.current"
      v-model:pageSize="dict.pagination.size"
      show-size-changer
      :total="dict.pagination.total"
      @change="async (page: number, pageSize: number) => {
        dict.pagination.current = page
        dict.pagination.size = pageSize
        await functions.refresh_app_list()
      }"
    />
  </div>
</template>

<style lang="less" scoped>
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

.title {
  opacity: 0.6;

  padding-top: 40px;
  margin-bottom: 40px;
}

.search_box {
  margin-bottom: 40px;
}

.a_table {
  margin-bottom: 30px;
}

.page_jumper {

}
</style>

<style lang="less">
.ant-table-thead .ant-table-cell {
  // background-color: rgba(144, 202, 249, 0.3);
  background-color: rgba(255, 235, 238);
  // background-color: rgba(245, 245, 245);
  // background-color: rgba(224, 224, 224);
  font-weight: bold;
}
</style>
