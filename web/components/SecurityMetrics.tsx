import React from 'react';
import { Card, Col, Row, Statistic } from 'antd';
import {
  AlertOutlined,
  AuditOutlined,
  BugOutlined,
  SafetyCertificateOutlined,
} from '@ant-design/icons';

interface SecurityMetricsProps {
  scansCompleted?: number;
  vulnerabilities?: number;
  incidents?: number;
  reports?: number;
}

const SecurityMetrics: React.FC<SecurityMetricsProps> = ({
  scansCompleted = 0,
  vulnerabilities = 0,
  incidents = 0,
  reports = 0,
}) => {
  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} sm={12} lg={6}>
        <Card bordered={false} style={{ background: '#1a1a2e' }}>
          <Statistic
            title="Scans Completed"
            value={scansCompleted}
            prefix={<SafetyCertificateOutlined style={{ color: '#52c41a' }} />}
            valueStyle={{ color: '#52c41a' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <Card bordered={false} style={{ background: '#1a1a2e' }}>
          <Statistic
            title="Vulnerabilities"
            value={vulnerabilities}
            prefix={<BugOutlined style={{ color: '#faad14' }} />}
            valueStyle={{ color: '#faad14' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <Card bordered={false} style={{ background: '#1a1a2e' }}>
          <Statistic
            title="Active Incidents"
            value={incidents}
            prefix={<AlertOutlined style={{ color: '#ff4d4f' }} />}
            valueStyle={{ color: '#ff4d4f' }}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} lg={6}>
        <Card bordered={false} style={{ background: '#1a1a2e' }}>
          <Statistic
            title="Reports Generated"
            value={reports}
            prefix={<AuditOutlined style={{ color: '#1890ff' }} />}
            valueStyle={{ color: '#1890ff' }}
          />
        </Card>
      </Col>
    </Row>
  );
};

export default SecurityMetrics;
