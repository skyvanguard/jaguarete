import AgentStatus from '@/components/AgentStatus';
import SecurityMetrics from '@/components/SecurityMetrics';
import { Divider, Layout, Space, Typography } from 'antd';
import { NextPage } from 'next';
import React from 'react';

const { Content } = Layout;
const { Title, Text } = Typography;

const Dashboard: NextPage = () => {
  return (
    <Layout style={{ minHeight: '100vh', background: '#0d0d1a' }}>
      <Content style={{ padding: '24px', maxWidth: 1200, margin: '0 auto', width: '100%' }}>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div>
            <Title level={2} style={{ color: '#fff', margin: 0 }}>
              Security Operations Dashboard
            </Title>
            <Text style={{ color: '#888' }}>Jaguarete - AI-Powered Purple Team Platform</Text>
          </div>

          <SecurityMetrics scansCompleted={42} vulnerabilities={7} incidents={2} reports={15} />

          <Divider style={{ borderColor: '#303050' }} />

          <AgentStatus />
        </Space>
      </Content>
    </Layout>
  );
};

export default Dashboard;
