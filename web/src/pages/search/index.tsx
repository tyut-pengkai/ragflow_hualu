import FileIcon from '@/components/file-icon';
import HightLightMarkdown from '@/components/highlight-markdown';
import { ImageWithPopover } from '@/components/image';
import PdfDrawer from '@/components/pdf-drawer';
import { useClickDrawer } from '@/components/pdf-drawer/hooks';
import RetrievalDocuments from '@/components/retrieval-documents';
import SvgIcon from '@/components/svg-icon';
import {
  useFetchKnowledgeList,
  useSelectTestingResult,
} from '@/hooks/knowledge-hooks';
import { useGetPaginationWithRouter } from '@/hooks/logic-hooks';
import { IReference } from '@/interfaces/database/chat';
import {
  Card,
  Divider,
  Flex,
  FloatButton,
  Input,
  Layout,
  List,
  Pagination,
  PaginationProps,
  Popover,
  Skeleton,
  Space,
  Spin,
  Tag,
  Tooltip,
  Typography,
} from 'antd';
import DOMPurify from 'dompurify';
import { isEmpty } from 'lodash';
import { useMemo, useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import MarkdownContent from '../chat/markdown-content';
import { useSendQuestion, useShowMindMapDrawer } from './hooks';
import styles from './index.less';
import MindMapDrawer from './mindmap-drawer';
import SearchSidebar from './sidebar';
import LogoImage from '@/icons/logodeep.png';

const { Content } = Layout;
const { Search } = Input;

const SearchPage = () => {
  const { t } = useTranslation();
  const [isInitialized, setIsInitialized] = useState(false);
  const [checkedList, setCheckedList] = useState<string[]>([]);
  const { chunks, total } = useSelectTestingResult();
  const { list: knowledgeList } = useFetchKnowledgeList();

  useEffect(() => {
    if (!isInitialized && knowledgeList.length > 0) {
      setCheckedList([knowledgeList[0].id]);
      setIsInitialized(true);
    }
  }, [knowledgeList, isInitialized]);

  const checkedWithoutEmbeddingIdList = useMemo(() => {
    return checkedList.filter((x) => knowledgeList.some((y) => y.id === x));
  }, [checkedList, knowledgeList]);

  const {
    sendQuestion,
    handleClickRelatedQuestion,
    handleSearchStrChange,
    handleTestChunk,
    setSelectedDocumentIds,
    answer,
    sendingLoading,
    relatedQuestions,
    searchStr,
    loading,
    isFirstRender,
    selectedDocumentIds,
    isSearchStrEmpty,
  } = useSendQuestion(checkedWithoutEmbeddingIdList);
  const { visible, hideModal, documentId, selectedChunk, clickDocumentButton } =
    useClickDrawer();
  const { pagination } = useGetPaginationWithRouter();
  const {
    mindMapVisible,
    hideMindMapModal,
    showMindMapModal,
    mindMapLoading,
    mindMap,
  } = useShowMindMapDrawer(checkedWithoutEmbeddingIdList, searchStr);

  const onChange: PaginationProps['onChange'] = (pageNumber, pageSize) => {
    pagination.onChange?.(pageNumber, pageSize);
    handleTestChunk(selectedDocumentIds, pageNumber, pageSize);
  };

  const InputSearch = (
    <Search
      value={searchStr}
      onChange={handleSearchStrChange}
      placeholder={t('header.search')}
      allowClear
      enterButton
      onSearch={sendQuestion}
      size="large"
      loading={sendingLoading}
      disabled={checkedWithoutEmbeddingIdList.length === 0}
      className={isFirstRender ? styles.globalInput : styles.partialInput}
    />
  );

  return (
    <>
      <Layout className={styles.searchPage}>
        <SearchSidebar
          isFirstRender={isFirstRender}
          checkedList={checkedWithoutEmbeddingIdList}
          setCheckedList={setCheckedList}
        ></SearchSidebar>
        <Layout className={isFirstRender ? styles.mainLayout : ''}>
          <Content>
            {isFirstRender ? (
              <Flex justify="center" >
                <Flex vertical align="center" gap={'middle'}>
                  <img src={LogoImage} alt="logo" style={{ width: '50%', marginTop: '150px' }} />
                  {InputSearch}
                  <Space direction="vertical" align="center" style={{ marginTop: '20px' }}>
                    <Typography.Text type="secondary">
                      大家好，欢迎使用华陆本地deepseek知识库，在这里在右侧选择目录，搜索公司相关知识并加以创作。
                      例如：根据公司2025年战略规划给我做一段工作总结<br/>
                      您也可以切换知识库进行生成生成。例如：点击右侧菜单切换至‘咨询部-产业政策专栏’ 搜索：根据陕西省2025年化工规划写一个煤化工的发展规划<br/>
                      目前我显卡还不够好，反应有些慢，请大家理解，如需要定制AI服务，可联系我的AI训练老师：信息中心 苗鑫禹  

                    </Typography.Text>
                    <Typography.Link href="/chat" style={{ fontSize: '14px' }}>
                      前往聊天页面开启AI聊天 →
                    </Typography.Link>
                    <Typography.Link href="/chat" style={{ fontSize: '14px' }}>
                      下载华陆微软office智能助手 →
                    </Typography.Link>
                    <Typography.Link href="/chat" style={{ fontSize: '14px' }}>
                      下载AI编程智能助手 →
                    </Typography.Link>
                  </Space>
                </Flex>
              </Flex>
            ) : (
              <Flex className={styles.content}>
                <section className={styles.main}>
                  {InputSearch}
                  <Card
                    title={
                      <Flex gap={10}>
                        <img src="/logo.svg" alt="" width={20} />
                        {t('chat.answerTitle')}
                      </Flex>
                    }
                    className={styles.answerWrapper}
                  >
                    {isEmpty(answer) && sendingLoading ? (
                      <Skeleton active />
                    ) : (
                      answer.answer && (
                        <MarkdownContent
                          loading={sendingLoading}
                          content={answer.answer}
                          reference={answer.reference ?? ({} as IReference)}
                          clickDocumentButton={clickDocumentButton}
                        ></MarkdownContent>
                      )
                    )}
                  </Card>
                  <Divider></Divider>
                  <RetrievalDocuments
                    selectedDocumentIds={selectedDocumentIds}
                    setSelectedDocumentIds={setSelectedDocumentIds}
                    onTesting={handleTestChunk}
                  ></RetrievalDocuments>
                  <Divider></Divider>
                  <Spin spinning={loading}>
                    {chunks?.length > 0 && (
                      <List
                        dataSource={chunks || []}
                        className={styles.chunks}
                        renderItem={(item) => (
                          <List.Item>
                            <Card className={styles.card}>
                              <Space>
                                <ImageWithPopover
                                  id={item.img_id}
                                ></ImageWithPopover>
                                <Flex vertical gap={10}>
                                  <Popover
                                    content={
                                      <div className={styles.popupMarkdown}>
                                        <HightLightMarkdown>
                                          {item.content_with_weight}
                                        </HightLightMarkdown>
                                      </div>
                                    }
                                  >
                                    <div
                                      dangerouslySetInnerHTML={{
                                        __html: DOMPurify.sanitize(
                                          `${item.highlight}...`,
                                        ),
                                      }}
                                      className={styles.highlightContent}
                                    ></div>
                                  </Popover>
                                  <Space
                                    className={styles.documentReference}
                                    onClick={() =>
                                      clickDocumentButton(
                                        item.doc_id,
                                        item as any,
                                      )
                                    }
                                  >
                                    <FileIcon
                                      id={item.image_id}
                                      name={item.docnm_kwd}
                                    ></FileIcon>
                                    {item.docnm_kwd}
                                  </Space>
                                </Flex>
                              </Space>
                            </Card>
                          </List.Item>
                        )}
                      />
                    )}
                  </Spin>
                  {relatedQuestions?.length > 0 && (
                    <Card title={t('chat.relatedQuestion')}>
                      <Flex wrap="wrap" gap={'10px 0'}>
                        {relatedQuestions?.map((x, idx) => (
                          <Tag
                            key={idx}
                            className={styles.tag}
                            onClick={handleClickRelatedQuestion(x)}
                          >
                            {x}
                          </Tag>
                        ))}
                      </Flex>
                    </Card>
                  )}
                  <Divider></Divider>
                  <Pagination
                    {...pagination}
                    total={total}
                    onChange={onChange}
                    className={styles.pagination}
                  />
                </section>
              </Flex>
            )}
          </Content>
        </Layout>
      </Layout>
      {!isFirstRender &&
        !isSearchStrEmpty &&
        !isEmpty(checkedWithoutEmbeddingIdList) && (
          <Tooltip title={t('chunk.mind')} zIndex={1}>
            {/* <FloatButton
              className={styles.mindMapFloatButton}
              onClick={showMindMapModal}
              icon={
                <SvgIcon name="paper-clip" width={24} height={30}></SvgIcon>
              }
            /> */}
          </Tooltip>
        )}
      {visible && (
        <PdfDrawer
          visible={visible}
          hideModal={hideModal}
          documentId={documentId}
          chunk={selectedChunk}
        ></PdfDrawer>
      )}
      {mindMapVisible && (
        <MindMapDrawer
          visible={mindMapVisible}
          hideModal={hideMindMapModal}
          data={mindMap}
          loading={mindMapLoading}
        ></MindMapDrawer>
      )}
    </>
  );
};

export default SearchPage;
